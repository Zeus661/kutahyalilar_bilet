import sys
sys.path.insert(0, "/shared")

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import router
from app.models import Base
from app.database import engine, SessionLocal
from app.service import create_profile_from_event
from shared.kafka_client import get_consumer


async def consume_user_registered():
    consumer = await get_consumer("user.registered", "user-service-group")
    try:
        async for msg in consumer:
            data = msg.value
            async with SessionLocal() as db:
                await create_profile_from_event(db, data["user_id"])
    finally:
        await consumer.stop()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    task = asyncio.create_task(consume_user_registered())
    yield
    task.cancel()
    await engine.dispose()


app = FastAPI(title="User Service", lifespan=lifespan)
app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "user-service"}
