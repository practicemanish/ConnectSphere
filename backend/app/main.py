"""Application entry point. Run with: uvicorn app.main:app --reload"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.db.session import engine
from app.modules.health.router import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Code before `yield` runs at startup, code after runs at shutdown.
    yield
    await engine.dispose()  # close pooled DB connections cleanly


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    # Every API route lives under /api so the frontend dev proxy can forward one prefix.
    app.include_router(health_router, prefix="/api")
    return app


app = create_app()
