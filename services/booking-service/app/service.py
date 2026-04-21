import secrets
import string
import os
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models import Booking
from app.schemas import BookingCreate

import sys
sys.path.insert(0, "/shared")
from shared.exceptions import not_found, bad_request


TRIP_SERVICE_HOST = os.environ.get("TRIP_SERVICE_HOST", "trip-service")
PAYMENT_SERVICE_HOST = os.environ.get("PAYMENT_SERVICE_HOST", "payment-service")


def generate_ticket_code() -> str:
    chars = string.ascii_uppercase + string.digits
    return "KT-" + "".join(secrets.choice(chars) for _ in range(8))


async def _call_trip_service(path: str, method: str = "GET", json_data: dict = None, token: str = ""):
    url = f"http://{TRIP_SERVICE_HOST}:8003{path}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    async with httpx.AsyncClient(timeout=10.0) as client:
        if method == "GET":
            resp = await client.get(url, headers=headers)
        else:
            resp = await client.post(url, headers=headers, json=json_data)
        return resp


async def _call_payment_service(data: dict, token: str = ""):
    url = f"http://{PAYMENT_SERVICE_HOST}:8005/api/v1/payments/"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(url, headers=headers, json=data)
        return resp


async def create_booking(
    db: AsyncSession,
    user_id: str,
    data: BookingCreate,
    token: str,
) -> Booking:
    # Step 2: Verify trip exists and seat is available
    seats_resp = await _call_trip_service(
        f"/api/v1/trips/{data.trip_id}/seats", token=token
    )
    if seats_resp.status_code != 200:
        bad_request("Could not fetch trip seats")
    seats = seats_resp.json()
    seat_info = None
    for s in seats:
        if s["id"] == str(data.seat_id):
            seat_info = s
            break
    if not seat_info:
        not_found("Seat")
    if seat_info["is_reserved"]:
        bad_request("Seat is already reserved")

    # Step 3: Reserve seat
    reserve_resp = await _call_trip_service(
        f"/api/v1/trips/{data.trip_id}/seats/{data.seat_id}/reserve",
        method="POST",
        token=token,
    )
    if reserve_resp.status_code != 200:
        bad_request("Could not reserve seat")

    # Get trip price
    trip_resp = await _call_trip_service(
        f"/api/v1/trips/{data.trip_id}", token=token
    )
    if trip_resp.status_code != 200:
        bad_request("Could not fetch trip details")
    trip_data = trip_resp.json()
    total_price = float(trip_data["price"])

    # Step 4: Create booking record
    booking = Booking(
        user_id=user_id,
        trip_id=data.trip_id,
        seat_id=data.seat_id,
        seat_number=seat_info["seat_number"],
        passenger_name=data.passenger_name,
        passenger_tc=data.passenger_tc,
        passenger_gender=data.passenger_gender,
        passenger_dob=data.passenger_dob,
        total_price=total_price,
        ticket_code=generate_ticket_code(),
        status="pending",
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    # Step 5: Initiate payment
    payment_resp = await _call_payment_service({
        "booking_id": str(booking.id),
        "user_id": user_id,
        "amount": total_price,
    }, token=token)

    if payment_resp.status_code == 201:
        payment_data = payment_resp.json()
        if payment_data["status"] == "completed":
            # Step 6: Payment success
            booking.status = "confirmed"
            booking.payment_id = payment_data["id"]
            await db.commit()
            await db.refresh(booking)

            # Step 7: Emit booking.created
            from shared.kafka_client import get_producer
            producer = await get_producer()
            try:
                await producer.send_and_wait("booking.created", {
                    "booking_id": str(booking.id),
                    "user_id": str(booking.user_id),
                    "trip_id": str(booking.trip_id),
                    "seat_number": booking.seat_number,
                    "ticket_code": booking.ticket_code,
                    "total_price": float(booking.total_price),
                })
            finally:
                await producer.stop()

            return booking

    # Step 8: Payment failure → release seat
    await _call_trip_service(
        f"/api/v1/trips/{data.trip_id}/seats/{data.seat_id}/release",
        method="POST",
        token=token,
    )
    booking.status = "cancelled"
    await db.commit()
    await db.refresh(booking)
    bad_request("Payment failed, booking cancelled")


async def cancel_booking(db: AsyncSession, booking_id: UUID, user_id: str, is_admin: bool, token: str):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        not_found("Booking")
    if not is_admin and str(booking.user_id) != user_id:
        bad_request("Not your booking")

    booking.status = "cancelled"
    await db.commit()
    await db.refresh(booking)

    # Release seat
    await _call_trip_service(
        f"/api/v1/trips/{booking.trip_id}/seats/{booking.seat_id}/release",
        method="POST",
        token=token,
    )

    # Emit booking.cancelled
    from shared.kafka_client import get_producer
    producer = await get_producer()
    try:
        await producer.send_and_wait("booking.cancelled", {
            "booking_id": str(booking.id),
            "user_id": str(booking.user_id),
            "trip_id": str(booking.trip_id),
            "seat_id": str(booking.seat_id),
        })
    finally:
        await producer.stop()

    return booking


async def get_booking(db: AsyncSession, booking_id: UUID):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        not_found("Booking")
    return booking


async def list_my_bookings(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(Booking).where(Booking.user_id == user_id)
    )
    return result.scalars().all()


async def list_all_bookings(db: AsyncSession):
    result = await db.execute(select(Booking))
    return result.scalars().all()
