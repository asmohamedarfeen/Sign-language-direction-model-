"""
Recognition Module Dependencies.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_db
from backend.recognition.repository.prediction_log_repository import PredictionLogRepository
from backend.recognition.service.recognition_service import RecognitionService


async def get_prediction_log_repository(
    db: AsyncSession = Depends(get_db)
) -> PredictionLogRepository:
    """Dependency providing PredictionLogRepository instance."""
    return PredictionLogRepository(db)


async def get_recognition_service(
    repo: PredictionLogRepository = Depends(get_prediction_log_repository)
) -> RecognitionService:
    """Dependency providing RecognitionService instance."""
    return RecognitionService(repo)
