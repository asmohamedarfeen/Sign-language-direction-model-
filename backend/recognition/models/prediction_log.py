"""
Prediction Log Database Model.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.core.database import Base


class PredictionLog(Base):
    """Stores individual model gesture predictions for quality audits and analytics."""

    __tablename__ = "recognition_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(64), index=True, nullable=True)
    predicted_sign = Column(String(32), index=True, nullable=False)
    confidence = Column(Float, nullable=False)
    latency_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
