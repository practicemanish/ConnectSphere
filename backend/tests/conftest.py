from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import get_settings
from app.main import app

BACKEND_DIR = Path(__file__).resolve().parents[1]


def get_test_database_url() -> str:
    """Same server as the dev DB, but the separate '<name>_test' database."""
    url = make_url(get_settings().database_url)
    test_url = url.set(database=f"{url.database}_test")
    # Safety net: tests create and drop tables, so they must never touch the dev DB.
    assert test_url.database is not None and test_url.database.endswith("_test")
    return test_url.render_as_string(hide_password=False)


def make_alembic_config(database_url: str) -> Config:
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    # '%' must be doubled because Config values go through ConfigParser interpolation.
    config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))
    return config


@pytest.fixture
def anyio_backend() -> str:
    # Run async tests on asyncio only (anyio would also try trio, which we don't use).
    return "asyncio"


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """HTTP client that calls the app in-process, no real server needed."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def migrated_test_db() -> Iterator[str]:
    """Test database upgraded to the latest migration. Returns its URL.

    Running the real migrations here means the tests also prove the migrations work.
    """
    url = get_test_database_url()
    command.upgrade(make_alembic_config(url), "head")
    yield url


@pytest.fixture
async def db_session(migrated_test_db: str) -> AsyncIterator[AsyncSession]:
    """Session on the test DB. Anything not committed is rolled back after the test."""
    engine = create_async_engine(migrated_test_db, poolclass=NullPool)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
        await session.rollback()
    await engine.dispose()
