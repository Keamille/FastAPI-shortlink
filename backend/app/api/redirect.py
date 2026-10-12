from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.deps import RedisDep
from app.services.shortlink import ShortlinkService

router = APIRouter(tags=["redirect"])


@router.get("/{code}")
async def redirect_short_code(code: str, redis: RedisDep) -> RedirectResponse:
    shortlink_service = ShortlinkService()
    original_url = await shortlink_service.resolve_and_click(code, redis)
    if not original_url:
        raise HTTPException(status_code=404, detail="short link not found")
    return RedirectResponse(url=original_url, status_code=302)
