from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import UserProfile
from app.schemas import ProfileUpdate

import sys
sys.path.insert(0, "/shared")
from shared.exceptions import not_found


async def get_profile(db: AsyncSession, auth_user_id: str) -> UserProfile:
    result = await db.execute(
        select(UserProfile).where(UserProfile.auth_user_id == auth_user_id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        not_found("Profile")
    return profile


async def update_profile(db: AsyncSession, auth_user_id: str, data: ProfileUpdate) -> UserProfile:
    profile = await get_profile(db, auth_user_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    await db.commit()
    await db.refresh(profile)
    return profile


async def create_profile_from_event(db: AsyncSession, auth_user_id: str):
    existing = await db.execute(
        select(UserProfile).where(UserProfile.auth_user_id == auth_user_id)
    )
    if existing.scalar_one_or_none():
        return
    profile = UserProfile(auth_user_id=auth_user_id)
    db.add(profile)
    await db.commit()
