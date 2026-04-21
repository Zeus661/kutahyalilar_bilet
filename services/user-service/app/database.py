import sys
sys.path.insert(0, "/shared")

from shared.database import make_engine, make_session_factory
import os

engine = make_engine(os.environ.get("DB_NAME", "user_db"))
SessionLocal = make_session_factory(engine)


async def get_db():
    async with SessionLocal() as session:
        yield session
