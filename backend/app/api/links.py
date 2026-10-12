from fastapi import APIRouter, status

from app.schemas.common import ApiResponse
from app.schemas.link import CreateLinkRequest, LinkItem, LinkListData

router = APIRouter(prefix="/api/v1/links", tags=["links"])


@router.post(
    "",
    response_model=ApiResponse[LinkItem],
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
async def create_link(body: CreateLinkRequest) -> ApiResponse[LinkItem]:
    """Create a short link — implement in ShortlinkService."""
    raise NotImplementedError("POST /api/v1/links not implemented yet")


@router.get("", response_model=ApiResponse[LinkListData])
async def list_links(
    page: int = 1,
    page_size: int = 20,
) -> ApiResponse[LinkListData]:
    raise NotImplementedError("GET /api/v1/links not implemented yet")


@router.get("/{code}", response_model=ApiResponse[LinkItem])
async def get_link(code: str) -> ApiResponse[LinkItem]:
    raise NotImplementedError("GET /api/v1/links/{code} not implemented yet")


@router.delete("/{code}", response_model=ApiResponse[None])
async def delete_link(code: str) -> ApiResponse[None]:
    raise NotImplementedError("DELETE /api/v1/links/{code} not implemented yet")
