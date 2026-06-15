"""
Sign Vocabulary Pydantic Schemas.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SignBase(BaseModel):
    symbol: str
    label: str
    category: str
    description: Optional[str] = None
    tips: Optional[str] = None
    image_url: Optional[str] = None


class SignCreate(SignBase):
    pass


class SignResponse(SignBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
