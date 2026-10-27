import uuid
from datetime import timedelta

import pytest
from sqlalchemy import delete
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User

pytestmark = pytest.mark.anyio


def make_user(**overrides: str) -> User:
    suffix = uuid.uuid4().hex[:8]
    fields = {
        "username": f"user_{suffix}",
        "email": f"user_{suffix}@example.com",
        "password_hash": "not-a-real-hash",
        "display_name": "Test User",
    }
    fields.update(overrides)
    return User(**fields)


async def test_defaults_are_filled_by_the_database(db_session: AsyncSession) -> None:
    user = make_user()
    db_session.add(user)
    await db_session.flush()  # sends INSERT ... RETURNING, no commit

    assert user.id.version == 7
    assert user.bio == ""
    assert user.created_at.tzinfo is not None  # timezone-aware
    assert user.updated_at.tzinfo is not None


async def test_duplicate_username_is_rejected(db_session: AsyncSession) -> None:
    db_session.add(make_user(username="same_name"))
    db_session.add(make_user(username="same_name"))

    with pytest.raises(IntegrityError, match="uq_users_username"):
        await db_session.flush()


async def test_duplicate_email_is_rejected(db_session: AsyncSession) -> None:
    db_session.add(make_user(email="same@example.com"))
    db_session.add(make_user(email="same@example.com"))

    with pytest.raises(IntegrityError, match="uq_users_email"):
        await db_session.flush()


@pytest.mark.parametrize(
    "username",
    ["Upper_Case", "ab", "has space", "bad-dash", "emoji_é"],
)
async def test_invalid_username_is_rejected(db_session: AsyncSession, username: str) -> None:
    db_session.add(make_user(username=username))

    with pytest.raises(IntegrityError, match="ck_users_username_format"):
        await db_session.flush()


async def test_uppercase_email_is_rejected(db_session: AsyncSession) -> None:
    db_session.add(make_user(email="Mixed@Example.com"))

    with pytest.raises(IntegrityError, match="ck_users_email_lowercase"):
        await db_session.flush()


@pytest.mark.parametrize("display_name", ["", "   "])
async def test_blank_display_name_is_rejected(db_session: AsyncSession, display_name: str) -> None:
    db_session.add(make_user(display_name=display_name))

    with pytest.raises(IntegrityError, match="ck_users_display_name_not_blank"):
        await db_session.flush()


async def test_too_long_username_is_rejected(db_session: AsyncSession) -> None:
    # Stopped by the VARCHAR(30) column type, before the CHECK constraint is reached.
    db_session.add(make_user(username="a" * 31))

    with pytest.raises(DBAPIError, match="too long"):
        await db_session.flush()


async def test_too_long_bio_is_rejected(db_session: AsyncSession) -> None:
    db_session.add(make_user(bio="x" * 161))

    with pytest.raises(DBAPIError, match="too long"):
        await db_session.flush()


async def test_updated_at_changes_on_update(db_session: AsyncSession) -> None:
    # now() is fixed per transaction, so this test needs two real commits.
    # It runs on the test database only, and deletes its row at the end.
    user = make_user()
    db_session.add(user)
    await db_session.commit()
    try:
        original = user.updated_at
        user.display_name = "Renamed"
        await db_session.commit()
        await db_session.refresh(user)

        assert user.updated_at > original
        assert user.updated_at - original < timedelta(minutes=1)
    finally:
        await db_session.execute(delete(User).where(User.id == user.id))
        await db_session.commit()
