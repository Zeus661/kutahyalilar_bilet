from datetime import date
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.schemas import (
    BusCreate,
    BusOut,
    RouteCreate,
    RouteOut,
    SeatOut,
    SeatReserveResponse,
    TripCreate,
    TripDetail,
    TripOut,
)
from app.service import (
    create_bus,
    create_route,
    create_trip,
    get_trip_detail,
    get_trip_seats,
    list_routes,
    release_seat,
    reserve_seat,
    search_trips,
)

router = APIRouter(tags=["trips"])


@router.get("/trips/search", response_model=List[TripOut])
async def search(
    origin: str = Query(...),
    destination: str = Query(...),
    date: date = Query(...),
    _user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await search_trips(db, origin, destination, date)


@router.get("/trips/{trip_id}", response_model=TripDetail)
async def trip_detail(
    trip_id: UUID, _user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    trip = await get_trip_detail(db, trip_id)
    seats = await get_trip_seats(db, trip_id)
    return TripDetail(
        **{c.name: getattr(trip, c.name) for c in trip.__table__.columns}, seats=seats
    )


@router.get("/trips/{trip_id}/seats", response_model=List[SeatOut])
async def trip_seats(
    trip_id: UUID, _user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await get_trip_seats(db, trip_id)


@router.post("/trips/", response_model=TripOut, status_code=201)
async def add_trip(
    data: TripCreate, _admin=Depends(require_admin), db: AsyncSession = Depends(get_db)
):
    return await create_trip(db, data)


@router.put("/trips/{trip_id}", response_model=TripOut)
async def update_trip(
    trip_id: UUID, _admin=Depends(require_admin), db: AsyncSession = Depends(get_db)
):
    from shared.exceptions import not_found

    not_found("Not implemented yet")


@router.delete("/trips/{trip_id}")
async def cancel_trip(
    trip_id: UUID, _admin=Depends(require_admin), db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import select, update

    from app.models import Trip

    stmt = update(Trip).where(Trip.id == trip_id).values(status="cancelled")
    await db.execute(stmt)
    await db.commit()
    return {"status": "cancelled"}


@router.post(
    "/trips/{trip_id}/seats/{seat_id}/reserve", response_model=SeatReserveResponse
)
async def reserve(
    trip_id: UUID,
    seat_id: UUID,
    _user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    seat = await reserve_seat(db, trip_id, seat_id)
    return SeatReserveResponse(
        seat_id=seat.id, trip_id=seat.trip_id, seat_number=seat.seat_number
    )


@router.post("/trips/{trip_id}/seats/{seat_id}/release")
async def release(
    trip_id: UUID,
    seat_id: UUID,
    _user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    seat = await release_seat(db, trip_id, seat_id)
    return {"status": "released", "seat_id": str(seat.id)}


@router.post("/routes/", response_model=RouteOut, status_code=201)
async def add_route(
    data: RouteCreate, _admin=Depends(require_admin), db: AsyncSession = Depends(get_db)
):
    return await create_route(db, data)


@router.get("/routes/", response_model=List[RouteOut])
async def get_routes(
    _user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await list_routes(db)


@router.post("/buses/", response_model=BusOut, status_code=201)
async def add_bus(
    data: BusCreate, _admin=Depends(require_admin), db: AsyncSession = Depends(get_db)
):
    return await create_bus(db, data)
