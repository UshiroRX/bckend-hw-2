import os
import redis.asyncio as redis  
from config import settings

redis_instance = None

async def get_redis() -> redis.Redis:
    global redis_instance
    if redis_instance is None:
        redis_instance = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
    return redis_instance
