from fastapi import APIRouter

from app.deps import SettingsDep
from app.schemas.common import ApiResponse

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(settings: SettingsDep) -> dict:
    """Liveness probe. Extend with Redis ping when wired up."""
    return {
        "status": "ok",
        "env": settings.app_env,
        "redis": "not_checked",
    }


@router.get("/api/v1/ping", response_model=ApiResponse[dict])
async def ping() -> ApiResponse[dict]:
    return ApiResponse(data={"pong": True})
