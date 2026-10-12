"""Shared FastAPI dependencies (e.g. Redis client).

Wire Redis here when you implement the shortlink service.
"""

from typing import Annotated

from fastapi import Depends

from app.config import Settings, get_settings
from redis.asyncio import Redis

SettingsDep = Annotated[Settings, Depends(get_settings)]

async def get_redis() -> Redis:
    return Redis.from_url(get_settings().redis_url,decode_responses=True)

RedisDep = Annotated[Redis, Depends(get_redis)]
