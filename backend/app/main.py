from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, links, redirect
from app.config import get_settings

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Per-request Redis is created in deps.get_redis(); keep lifespan light for now.
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Shortlink API",
        version="0.1.0",
        description="Long URL to short link microservice (Redis-only MVP)",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(links.router)
    # Register redirect last so /api and /health win over /{code}
    app.include_router(redirect.router)
    return app


app = create_app()
