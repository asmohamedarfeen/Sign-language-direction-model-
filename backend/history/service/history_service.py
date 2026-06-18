"""
History Service.

Business logic for managing translation logs, exports, and statistics.
"""

from typing import List, Optional
from backend.history.repository.history_repository import HistoryRepository
from backend.history.models.history import TranslationSession
from backend.history.schemas.history import SessionCreate, SessionStatsResponse


class HistoryService:
    """Service handling history tracking and metrics."""

    def __init__(self, repository: HistoryRepository):
        self.repo = repository

    async def record_session(self, session_data: SessionCreate) -> TranslationSession:
        """Stores a finalized translation session."""
        return await self.repo.create(session_data)

    async def list_sessions(self, limit: int = 50, offset: int = 0) -> List[TranslationSession]:
        """Returns paginated history records."""
        return await self.repo.get_all(limit=limit, offset=offset)

    async def remove_session(self, session_id: int) -> bool:
        """Deletes a history record by ID."""
        return await self.repo.delete(session_id)

    async def get_summary_stats(self) -> SessionStatsResponse:
        """Computes aggregate translation statistics."""
        raw_stats = await self.repo.get_stats()
        sessions = await self.repo.get_all(limit=1000)

        # Count total words
        total_words = sum(
            len(s.translated_text.strip().split())
            for s in sessions
            if s.translated_text.strip()
        )

        return SessionStatsResponse(
            total_sessions=raw_stats["total_sessions"],
            total_words_translated=total_words,
            overall_avg_confidence=raw_stats["avg_confidence"],
            total_gestures_processed=raw_stats["total_gestures"]
        )
