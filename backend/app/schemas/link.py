from pydantic import BaseModel, Field, HttpUrl


class CreateLinkRequest(BaseModel):
    url: HttpUrl
    ttl_seconds: int | None = Field(default=None, ge=1, le=31_536_000)


class LinkItem(BaseModel):
    code: str
    original_url: str
    short_url: str
    created_at: int
    ttl_seconds: int | None = None
    clicks: int = 0


class LinkListData(BaseModel):
    items: list[LinkItem]
    total: int
    page: int
    page_size: int
