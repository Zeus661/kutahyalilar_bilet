from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from datetime import date
from uuid import UUID

from app.models import Trip, Route, Bus, Seat
from app.schemas import TripCreate, RouteCreate, BusCreate

import sys
sys.path.insert(0, "/shared")
from shared.exceptions import not_found, conflict


async def search_trips(db: AsyncSession, origin: str, destination: str, trip_date: date):
    stmt = (
        select(Trip)
        .join(Route, Trip.route_id == Route.id)
        .where(
            and_(
                Route.origin == origin,
                Route.destination == destination,
                Trip.status == "scheduled"
            )
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_trip_detail(db: AsyncSession, trip_id: UUID):
    stmt = select(Trip).where(Trip.id == trip_id)
    result = await db.execute(stmt)
    trip = result.scalar_one_or_none()
    if not trip:
        not_found("Trip")
    return trip


async def get_trip_seats(db: AsyncSession, trip_id: UUID):
    result = await db.execute(
        select(Seat).where(Seat.trip_id == trip_id).order_by(Seat.seat_number)
    )
    return result.scalars().all()


async def create_trip(db: AsyncSession, data: TripCreate):
    bus_result = await db.execute(select(Bus).where(Bus.id == data.bus_id))
    bus = bus_result.scalar_one_or_none()
    if not bus:
        not_found("Bus")

    trip = Trip(
        route_id=data.route_id,
        bus_id=data.bus_id,
        departure_time=data.departure_time,
        arrival_time=data.arrival_time,
        price=data.price,
        available_seats=bus.total_seats,
    )
    db.add(trip)
    await db.flush()

    for i in range(1, bus.total_seats + 1):
        seat = Seat(trip_id=trip.id, seat_number=i)
        db.add(seat)

    await db.commit()
    await db.refresh(trip)
    return trip


async def reserve_seat(db: AsyncSession, trip_id: UUID, seat_id: UUID):
    stmt = select(Seat).where(
        and_(Seat.trip_id == trip_id, Seat.id == seat_id)
    ).with_for_update(skip_locked=True)
    result = await db.execute(stmt)
    seat = result.scalar_one_or_none()
    if not seat:
        not_found("Seat")
    if seat.is_reserved:
        conflict("Seat already reserved")

    seat.is_reserved = True
    trip_result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = trip_result.scalar_one()
    trip.available_seats -= 1
    await db.commit()
    await db.refresh(seat)
    return seat


async def release_seat(db: AsyncSession, trip_id: UUID, seat_id: UUID):
    stmt = select(Seat).where(
        and_(Seat.trip_id == trip_id, Seat.id == seat_id)
    )
    result = await db.execute(stmt)
    seat = result.scalar_one_or_none()
    if not seat:
        not_found("Seat")

    seat.is_reserved = False
    trip_result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = trip_result.scalar_one()
    trip.available_seats += 1
    await db.commit()
    return seat


async def create_route(db: AsyncSession, data: RouteCreate):
    route = Route(**data.model_dump())
    db.add(route)
    await db.commit()
    await db.refresh(route)
    return route


async def list_routes(db: AsyncSession):
    result = await db.execute(select(Route))
    return result.scalars().all()


async def create_bus(db: AsyncSession, data: BusCreate):
    bus = Bus(**data.model_dump())
    db.add(bus)
    await db.commit()
    await db.refresh(bus)
    return bus
