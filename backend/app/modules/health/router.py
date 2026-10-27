import logging

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.health.schemas import HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health(response: Response, db: AsyncSession = Depends(get_db)) -> HealthResponse:
    """Report whether the API is up and can reach the database."""
    try:
        await db.execute(text("SELECT 1"))
    except (SQLAlchemyError, OSError):
        # OSError covers "connection refused" and timeouts raised by the driver.
        logger.exception("Health check: database unreachable")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse(status="degraded", database="unavailable")
    return HealthResponse(status="ok", database="ok")
