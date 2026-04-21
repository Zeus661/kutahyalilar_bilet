from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models import UserProfile
from app.schemas import ProfileOut, ProfileUpdate
from app.service import create_profile_from_event, get_profile, update_profile

router = APIRouter(tags=["users"])


@router.get("/users/me", response_model=ProfileOut)
async def get_me(
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await get_profile(db, current_user["user_id"])


@router.put("/users/me", response_model=ProfileOut)
async def update_me(
    data: ProfileUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await update_profile(db, current_user["user_id"], data)


@router.get("/users/{user_id}", response_model=ProfileOut)
async def get_user(
    user_id: str, _admin=Depends(require_admin), db: AsyncSession = Depends(get_db)
):
    return await get_profile(db, user_id)


@router.get("/users/", response_model=List[ProfileOut])
async def list_users(_admin=Depends(require_admin), db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select

    result = await db.execute(select(UserProfile))
    return result.scalars().all()


@router.post(
    "/internal/users/bootstrap-profile", response_model=ProfileOut, status_code=201
)
async def bootstrap_profile(
    user_id: str,
    x_internal_token: str = Header(default=""),
    db: AsyncSession = Depends(get_db),
):
    import os

    expected = os.environ.get("INTERNAL_SERVICE_TOKEN", "dev-internal-token")
    if x_internal_token != expected:
        raise HTTPException(status_code=403, detail="Forbidden")
    await create_profile_from_event(db, user_id)
    return await get_profile(db, user_id)
