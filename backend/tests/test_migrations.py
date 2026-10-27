import asyncio

from alembic import command
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from tests.conftest import make_alembic_config

# Plain (sync) tests on purpose: Alembic's env.py starts its own event loop,
# which would clash with an already-running one.


def _table_names(database_url: str) -> set[str]:
    async def fetch() -> set[str]:
        engine = create_async_engine(database_url, poolclass=NullPool)
        try:
            async with engine.connect() as conn:
                return set(await conn.run_sync(lambda c: inspect(c).get_table_names()))
        finally:
            await engine.dispose()

    return asyncio.run(fetch())


def test_upgrade_creates_users_table(migrated_test_db: str) -> None:
    assert {"users", "alembic_version"} <= _table_names(migrated_test_db)


def test_models_and_migrations_are_in_sync(migrated_test_db: str) -> None:
    # command.check raises if autogenerate would produce any change,
    # i.e. someone changed a model without writing a migration.
    command.check(make_alembic_config(migrated_test_db))


def test_downgrade_and_upgrade_roundtrip(migrated_test_db: str) -> None:
    config = make_alembic_config(migrated_test_db)
    try:
        command.downgrade(config, "base")
        assert "users" not in _table_names(migrated_test_db)
    finally:
        command.upgrade(config, "head")  # always leave the test DB at head
    assert "users" in _table_names(migrated_test_db)
