import pytest
from httpx import AsyncClient

from app.db.session import get_db
from app.main import app

pytestmark = pytest.mark.anyio


async def test_health_ok_when_database_reachable(client: AsyncClient) -> None:
    # Integration test: needs the Docker database running (docker compose up -d db).
    response = await client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


async def test_health_degraded_when_database_down(client: AsyncClient) -> None:
    class BrokenSession:
        async def execute(self, *args, **kwargs):
            raise ConnectionRefusedError("simulated: database is down")

    async def broken_db():
        yield BrokenSession()

    # Dependency injection lets the test swap the real DB session for a fake one.
    app.dependency_overrides[get_db] = broken_db

    response = await client.get("/api/health")

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "database": "unavailable"}
