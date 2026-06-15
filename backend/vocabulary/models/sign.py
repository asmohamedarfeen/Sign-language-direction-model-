"""
Sign Vocabulary Database Model.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from backend.core.database import Base


class Sign(Base):
    """Represents a supported sign language symbol or word."""

    __tablename__ = "vocabulary_signs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    symbol = Column(String(32), unique=True, index=True, nullable=False)
    label = Column(String(64), nullable=False)
    category = Column(String(32), index=True, nullable=False)  # alphabet, word, control
    description = Column(Text, nullable=True)
    tips = Column(Text, nullable=True)
    image_url = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
