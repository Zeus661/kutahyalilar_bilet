from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os


def make_engine(db_name: str):
    url = (
        f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}"
        f":{os.environ['POSTGRES_PASSWORD']}"
        f"@{os.environ['POSTGRES_HOST']}"
        f":{os.environ['POSTGRES_PORT']}"
        f"/{db_name}"
    )
    return create_async_engine(url, echo=False, pool_pre_ping=True)


def make_session_factory(engine):
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
