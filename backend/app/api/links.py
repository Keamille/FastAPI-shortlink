from fastapi import APIRouter, HTTPException

from app.deps import RedisDep, SettingsDep
from app.schemas.common import ApiResponse
from app.schemas.link import CreateLinkRequest, LinkItem, LinkListData
from app.services.shortlink import ShortlinkService

router = APIRouter(prefix="/api/v1/links", tags=["links"])


def _map_value_error(exc: ValueError) -> HTTPException:
    msg = str(exc)
    if "not found" in msg.lower():
        return HTTPException(status_code=404, detail=msg)
    if "already exists" in msg.lower():
        return HTTPException(status_code=409, detail=msg)
    return HTTPException(status_code=400, detail=msg)


@router.post("", response_model=ApiResponse[LinkItem])
async def create_link(
    body: CreateLinkRequest,
    redis: RedisDep,
    settings: SettingsDep,
) -> ApiResponse[LinkItem]:
    shortlink_service = ShortlinkService()
    try:
        item = await shortlink_service.create_link(body, redis, settings)
    except ValueError as exc:
        raise _map_value_error(exc) from exc
    return ApiResponse(data=item)


@router.get("", response_model=ApiResponse[LinkListData])
async def list_links(
    redis: RedisDep,
    page: int = 1,
    page_size: int = 20,
) -> ApiResponse[LinkListData]:
    shortlink_service = ShortlinkService()
    return ApiResponse(data=await shortlink_service.list_links(page, page_size, redis))


@router.get("/{code}", response_model=ApiResponse[LinkItem])
async def get_link(code: str, redis: RedisDep) -> ApiResponse[LinkItem]:
    shortlink_service = ShortlinkService()
    try:
        item = await shortlink_service.get_link(code, redis)
    except ValueError as exc:
        raise _map_value_error(exc) from exc
    return ApiResponse(data=item)


@router.delete("/{code}", response_model=ApiResponse[None])
async def delete_link(code: str, redis: RedisDep) -> ApiResponse[None]:
    shortlink_service = ShortlinkService()
    await shortlink_service.delete_link(code, redis)
    return ApiResponse(data=None)
