from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.dependencies import get_current_user, require_admin
from app.schemas import ProfileUpdate, ProfileOut
from app.service import get_profile, update_profile
from app.models import UserProfile
from app.database import get_db

router = APIRouter(tags=["users"])


@router.get("/users/me", response_model=ProfileOut)
async def get_me(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_profile(db, current_user["user_id"])


@router.put("/users/me", response_model=ProfileOut)
async def update_me(
    data: ProfileUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await update_profile(db, current_user["user_id"], data)


@router.get("/users/{user_id}", response_model=ProfileOut)
async def get_user(user_id: str, _admin=Depends(require_admin), db: AsyncSession = Depends(get_db)):
    return await get_profile(db, user_id)


@router.get("/users/", response_model=List[ProfileOut])
async def list_users(_admin=Depends(require_admin), db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(UserProfile))
    return result.scalars().all()
