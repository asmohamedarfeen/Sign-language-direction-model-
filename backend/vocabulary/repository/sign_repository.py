"""
Sign Vocabulary Repository.

Encapsulates database operations for vocabulary signs.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.vocabulary.models.sign import Sign
from backend.vocabulary.schemas.sign import SignCreate


class SignRepository:
    """Repository handling sign entity persistence."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, category: Optional[str] = None) -> List[Sign]:
        """Retrieves all signs, optionally filtered by category."""
        query = select(Sign).order_by(Sign.id.asc())
        if category:
            query = query.where(Sign.category == category)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_symbol(self, symbol: str) -> Optional[Sign]:
        """Finds a single sign by its unique symbol."""
        query = select(Sign).where(Sign.symbol == symbol)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create(self, sign_data: SignCreate) -> Sign:
        """Inserts a new sign record."""
        sign = Sign(**sign_data.model_dump())
        self.db.add(sign)
        await self.db.flush()
        await self.db.refresh(sign)
        return sign

    async def count(self) -> int:
        """Returns the total number of signs."""
        query = select(Sign)
        result = await self.db.execute(query)
        return len(result.scalars().all())
