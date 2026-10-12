from fastapi import APIRouter

from app.deps import SettingsDep
from app.schemas.common import ApiResponse
from app.deps import get_redis
router = APIRouter(tags=["health"])


@router.get("/health")
async def health(settings: SettingsDep) -> dict:
    """Liveness probe. Extend with Redis ping when wired up."""
    redis = await get_redis()
    redis_status = await redis.ping()
    return {
        "status": "ok",
        "env": redis_status,
        "redis": "not_checked",
    }


@router.get("/api/v1/ping", response_model=ApiResponse[dict])
async def ping() -> ApiResponse[dict]:
    return ApiResponse(data={"pong": True})
