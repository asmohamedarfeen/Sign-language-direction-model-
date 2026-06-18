"""
Recognition Request & Response Schemas.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class LandmarkPoint(BaseModel):
    """Single 3D joint coordinate."""
    x: float
    y: float
    z: float = 0.0


class GesturePredictRequest(BaseModel):
    """Payload containing 21 MediaPipe hand landmarks."""
    landmarks: List[LandmarkPoint] = Field(..., min_length=21, max_length=21)
    handedness: str = Field(default="Right", description="'Right' or 'Left'")
    session_id: Optional[str] = None


class GestureCandidate(BaseModel):
    label: str
    confidence: float
    percentage: float


class GesturePredictResponse(BaseModel):
    """Model inference output."""
    predicted_sign: str
    confidence: float
    percentage: float
    top_candidates: List[GestureCandidate]
    current_sentence: str
    latency_ms: float
    is_stable: bool


class ResetSentenceRequest(BaseModel):
    session_id: Optional[str] = None


class SentenceStateResponse(BaseModel):
    session_id: str
    current_sentence: str
    character_count: int
    word_count: int
