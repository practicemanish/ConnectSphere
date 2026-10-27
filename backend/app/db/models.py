"""Imports every model so they register on Base.metadata.

Alembic's autogenerate only sees tables that were imported. Add each new module's
models here when it is created.
"""

from app.modules.users.models import User

__all__ = ["User"]
