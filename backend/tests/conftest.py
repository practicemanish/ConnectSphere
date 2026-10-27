from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


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
