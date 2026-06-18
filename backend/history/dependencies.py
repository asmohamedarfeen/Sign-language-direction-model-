"""
History Module Dependencies.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_db
from backend.history.repository.history_repository import HistoryRepository
from backend.history.service.history_service import HistoryService


async def get_history_repository(
    db: AsyncSession = Depends(get_db)
) -> HistoryRepository:
    """Dependency providing HistoryRepository instance."""
    return HistoryRepository(db)


async def get_history_service(
    repo: HistoryRepository = Depends(get_history_repository)
) -> HistoryService:
    """Dependency providing HistoryService instance."""
    return HistoryService(repo)
