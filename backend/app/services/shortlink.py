"""Shortlink Redis CRUD and redirect helpers.

Implement create / get / list / delete / resolve_and_click here.

create_link flow (docs §3.2):
- if body.custom_code: validate → ensure unique (SET NX / EXISTS) → use as code
- else: INCR seq → to_base62 → use as code
- then write code / meta / index (with optional TTL)
"""

from redis.asyncio import Redis
from app.schemas.link import CreateLinkRequest, LinkItem, LinkListData
from app.services.base62 import is_valid_custom_code, to_base62
from app.deps import RedisDep,SettingsDep
import time
class ShortlinkService:
    """Skeleton service — fill in Redis operations yourself."""

    async def create_link(self, body: CreateLinkRequest,redis: Redis,settings: SettingsDep) -> LinkItem:
        code = ""
        if body.custom_code:
            if not is_valid_custom_code(body.custom_code):
                raise ValueError("Invalid custom code")
            if await redis.exists(f"short_url:code:{body.custom_code}"):
                raise ValueError("Custom code already exists")
            code =body.custom_code
        else:
            code = to_base62(await redis.incr("seq"))
            while await redis.exists(f"short_url:code:{code}"):
                code = to_base62(await redis.incr("seq"))
        short_url = f"{settings.base_url}/{code}"
        original_url = str(body.url)
        created_at = int(time.time())
        if body.ttl_seconds:
            ttl_seconds = body.ttl_seconds
        else:
            ttl_seconds = 7 * 24 * 60 * 60

        await redis.set(f"short_url:code:{code}", short_url, ex=ttl_seconds)
        await redis.set(f"original_url:code:{code}", original_url, ex=ttl_seconds)
        await redis.set(f"created_at:code:{code}", created_at, ex=ttl_seconds)
        await redis.set(f"click_count:code:{code}", 0, ex=ttl_seconds)

        return LinkItem(
            code=code,
            original_url=original_url,
            short_url=short_url,
            created_at=created_at,
            ttl_seconds=ttl_seconds,
        )



    async def get_link(self, code: str, redis: Redis) -> LinkItem:
        short_url = await redis.get(f"short_url:code:{code}")
        original_url = await redis.get(f"original_url:code:{code}")
        created_at = await redis.get(f"created_at:code:{code}")
        ttl_seconds = await redis.ttl(f"short_url:code:{code}")
        if not short_url or not original_url or created_at is None:
            raise ValueError("Short link not found")
        return LinkItem(
            code=code,
            original_url=original_url,
            short_url=short_url,
            created_at=int(created_at),
            ttl_seconds=ttl_seconds if ttl_seconds and ttl_seconds > 0 else None,
        )

    async def list_links(self, page: int, page_size: int, redis: Redis) -> LinkListData:
        items: list[LinkItem] = []
        for key in await redis.keys("short_url:code:*"):
            code = key.split(":")[-1]
            short_url = await redis.get(f"short_url:code:{code}")
            original_url = await redis.get(f"original_url:code:{code}")
            created_at = await redis.get(f"created_at:code:{code}")
            ttl_seconds = await redis.ttl(f"short_url:code:{code}")
            if not short_url or not original_url or created_at is None:
                continue
            items.append(
                LinkItem(
                    code=code,
                    original_url=original_url,
                    short_url=short_url,
                    created_at=int(created_at),
                    ttl_seconds=ttl_seconds if ttl_seconds and ttl_seconds > 0 else None,
                )
            )
        total = len(items)
        start = max(page - 1, 0) * page_size
        end = start + page_size
        return LinkListData(
            items=items[start:end],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def delete_link(self, code: str, redis: Redis) -> None:
        await redis.delete(f"short_url:code:{code}")
        await redis.delete(f"original_url:code:{code}")
        await redis.delete(f"created_at:code:{code}")
        await redis.delete(f"click_count:code:{code}")

    async def resolve_and_click(self, code: str,redis: Redis) -> str:
        """Return original URL and increment click count."""
        original_url = await redis.get(f"original_url:code:{code}")
        await redis.incr(f"click_count:code:{code}")
        return original_url
