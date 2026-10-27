"""Database engine and the per-request session dependency."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

# One engine per process. It owns the connection pool.
engine = create_async_engine(
    get_settings().database_url,
    pool_pre_ping=True,  # test a pooled connection before using it
    connect_args={"timeout": 5},  # asyncpg waits 60s by default when the DB is down
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency: one session per request, always closed afterwards."""
    async with SessionLocal() as session:
        yield session
