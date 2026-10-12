from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["redirect"])


@router.get("/{code}")
async def redirect_short_code(code: str) -> RedirectResponse:
    """Public 302 redirect — implement resolve_and_click then return Location."""
    raise NotImplementedError("GET /{code} redirect not implemented yet")
