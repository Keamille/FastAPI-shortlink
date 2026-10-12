"""Shortlink Redis CRUD and redirect helpers.

Implement create / get / list / delete / resolve_and_click here.
"""

from app.schemas.link import CreateLinkRequest, LinkItem, LinkListData


class ShortlinkService:
    """Skeleton service — fill in Redis operations yourself."""

    async def create_link(self, body: CreateLinkRequest) -> LinkItem:
        raise NotImplementedError

    async def get_link(self, code: str) -> LinkItem:
        raise NotImplementedError

    async def list_links(self, page: int, page_size: int) -> LinkListData:
        raise NotImplementedError

    async def delete_link(self, code: str) -> None:
        raise NotImplementedError

    async def resolve_and_click(self, code: str) -> str:
        """Return original URL and increment click count."""
        raise NotImplementedError
