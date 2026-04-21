import os

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import LoginRequest, RegisterRequest, TokenResponse, UserOut
from app.service import authenticate_user, create_access_token, register_user

router = APIRouter(tags=["auth"])


@router.post("/auth/register", status_code=201, response_model=UserOut)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = await register_user(db, data)

    user_service_host = os.environ.get("USER_SERVICE_HOST", "user-service")
    user_service_port = os.environ.get("USER_SERVICE_PORT", "8002")
    internal_token = os.environ.get("INTERNAL_SERVICE_TOKEN", "dev-internal-token")
    bootstrap_url = f"http://{user_service_host}:{user_service_port}/api/v1/internal/users/bootstrap-profile"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                bootstrap_url,
                params={"user_id": str(user.id)},
                headers={"X-Internal-Token": internal_token},
            )
    except Exception:
        pass

    from shared.kafka_client import get_producer

    producer = await get_producer()
    try:
        await producer.send_and_wait(
            "user.registered",
            {"user_id": str(user.id), "email": user.email, "event": "user.registered"},
        )
    finally:
        await producer.stop()

    return user


@router.post("/auth/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, data.email, data.password)
    token = create_access_token(str(user.id), user.email, user.is_admin)
    return TokenResponse(access_token=token)


@router.get("/auth/me", response_model=UserOut)
async def me(
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import select

    result = await db.execute(select(User).where(User.id == current_user["user_id"]))
    user = result.scalar_one_or_none()
    if not user:
        from shared.exceptions import not_found

        not_found("User")
    return user


@router.post("/auth/refresh", response_model=TokenResponse)
async def refresh(current_user=Depends(get_current_user)):
    token = create_access_token(
        current_user["user_id"], current_user["email"], current_user["is_admin"]
    )
    return TokenResponse(access_token=token)
