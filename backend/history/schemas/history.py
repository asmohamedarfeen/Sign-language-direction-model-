"""
History Schemas.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class SessionCreate(BaseModel):
    session_id: str
    translated_text: str = Field(..., min_length=1)
    total_gestures: int = Field(default=0, ge=0)
    avg_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    duration_seconds: float = Field(default=0.0, ge=0.0)


class SessionResponse(BaseModel):
    id: int
    session_id: str
    translated_text: str
    total_gestures: int
    avg_confidence: float
    duration_seconds: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionStatsResponse(BaseModel):
    total_sessions: int
    total_words_translated: int
    overall_avg_confidence: float
    total_gestures_processed: int
