"""
Translation History Database Model.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from backend.core.database import Base


class TranslationSession(Base):
    """Stores completed sign language translation sessions."""

    __tablename__ = "translation_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(64), index=True, nullable=False)
    translated_text = Column(Text, nullable=False)
    total_gestures = Column(Integer, default=0, nullable=False)
    avg_confidence = Column(Float, default=0.0, nullable=False)
    duration_seconds = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
