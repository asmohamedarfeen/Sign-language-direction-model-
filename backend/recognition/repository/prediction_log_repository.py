"""
Prediction Log Repository.
"""

from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from backend.recognition.models.prediction_log import PredictionLog


class PredictionLogRepository:
    """Handles logging and querying of recognition events."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_prediction(
        self,
        predicted_sign: str,
        confidence: float,
        latency_ms: float,
        session_id: Optional[str] = None
    ) -> PredictionLog:
        """Saves a prediction record."""
        log_entry = PredictionLog(
            session_id=session_id,
            predicted_sign=predicted_sign,
            confidence=confidence,
            latency_ms=latency_ms
        )
        self.db.add(log_entry)
        await self.db.flush()
        return log_entry

    async def get_recent_logs(self, limit: int = 50) -> List[PredictionLog]:
        """Returns the most recent predictions."""
        query = select(PredictionLog).order_by(desc(PredictionLog.created_at)).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
