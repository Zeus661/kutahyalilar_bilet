from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.dependencies import get_current_user, require_admin
from app.schemas import BookingCreate, BookingOut
from app.service import create_booking, cancel_booking, get_booking, list_my_bookings, list_all_bookings
from app.database import get_db

router = APIRouter(tags=["bookings"])


@router.post("/bookings/", response_model=BookingOut, status_code=201)
async def create(
    data: BookingCreate,
    request: Request,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    return await create_booking(db, current_user["user_id"], data, token)


@router.get("/bookings/my", response_model=List[BookingOut])
async def my_bookings(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await list_my_bookings(db, current_user["user_id"])


@router.get("/bookings/{booking_id}", response_model=BookingOut)
async def booking_detail(booking_id: UUID, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_booking(db, booking_id)


@router.delete("/bookings/{booking_id}", response_model=BookingOut)
async def cancel(
    booking_id: UUID,
    request: Request,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    return await cancel_booking(
        db, booking_id, current_user["user_id"], current_user["is_admin"], token
    )


@router.get("/bookings/", response_model=List[BookingOut])
async def all_bookings(_admin=Depends(require_admin), db: AsyncSession = Depends(get_db)):
    return await list_all_bookings(db)
