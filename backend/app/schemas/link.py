from pydantic import BaseModel, Field, HttpUrl, field_validator


class CreateLinkRequest(BaseModel):
    url: HttpUrl
    custom_code: str | None = Field(
        default=None,
        min_length=3,
        max_length=32,
        description="Optional custom short code (Base62). Omit to auto-generate.",
    )
    ttl_seconds: int | None = Field(default=None, ge=1, le=31_536_000)

    @field_validator("custom_code")
    @classmethod
    def normalize_custom_code(cls, v: str | None) -> str | None:
        if v is None:
            return None
        code = v.strip()
        return code or None


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
