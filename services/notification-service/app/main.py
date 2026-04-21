from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.consumer import start_consumers


@asynccontextmanager
async def lifespan(app: FastAPI):
    tasks = start_consumers()
    yield
    for task in tasks:
        task.cancel()


app = FastAPI(title="Notification Service", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "notification-service"}
