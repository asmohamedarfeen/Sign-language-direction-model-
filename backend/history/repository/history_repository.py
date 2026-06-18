"""
History Repository.
"""

from typing import List, Optional
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from backend.history.models.history import TranslationSession
from backend.history.schemas.history import SessionCreate


class HistoryRepository:
    """Handles persistence and retrieval of translation session history."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, session_data: SessionCreate) -> TranslationSession:
        """Saves a completed session."""
        session = TranslationSession(**session_data.model_dump())
        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)
        return session

    async def get_all(self, limit: int = 50, offset: int = 0) -> List[TranslationSession]:
        """Retrieves history ordered newest first."""
        query = (
            select(TranslationSession)
            .order_by(desc(TranslationSession.created_at))
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, session_id: int) -> Optional[TranslationSession]:
        """Finds session by database primary key ID."""
        query = select(TranslationSession).where(TranslationSession.id == session_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def delete(self, session_id: int) -> bool:
        """Deletes a session record."""
        session = await self.get_by_id(session_id)
        if not session:
            return False
        await self.db.delete(session)
        await self.db.flush()
        return True

    async def get_stats(self) -> dict:
        """Aggregates metrics across all recorded sessions."""
        query = select(
            func.count(TranslationSession.id).label("total_sessions"),
            func.coalesce(func.sum(TranslationSession.total_gestures), 0).label("total_gestures"),
            func.coalesce(func.avg(TranslationSession.avg_confidence), 0.0).label("avg_confidence")
        )
        result = await self.db.execute(query)
        row = result.first()
        return {
            "total_sessions": row.total_sessions if row else 0,
            "total_gestures": row.total_gestures if row else 0,
            "avg_confidence": round(float(row.avg_confidence), 4) if row else 0.0
        }
