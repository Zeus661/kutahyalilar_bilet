import sys
sys.path.insert(0, "/shared")

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import router
from app.models import Base
from app.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Auth Service", lifespan=lifespan)
app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "auth-service"}
