import redis.asyncio as aioredis
import os


def get_redis():
    return aioredis.from_url(
        f"redis://{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}",
        decode_responses=True
    )
