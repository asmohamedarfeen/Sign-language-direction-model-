"""
Sign Vocabulary Service.

Encapsulates business logic for vocabulary retrieval and seed initialization.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.vocabulary.repository.sign_repository import SignRepository
from backend.vocabulary.models.sign import Sign
from backend.vocabulary.schemas.sign import SignCreate
from backend.vocabulary.constants import DEFAULT_SIGNS
from backend.core.logging import logger


class SignService:
    """Service providing sign vocabulary functionality."""

    def __init__(self, repository: SignRepository):
        self.repo = repository

    async def list_signs(self, category: Optional[str] = None) -> List[Sign]:
        """Returns all signs, auto-seeding if empty or out of sync."""
        signs = await self.repo.get_all(category=category)
        if not signs and category is None:
            await self.seed_default_signs()
            signs = await self.repo.get_all(category=category)
        return signs

    async def get_sign(self, symbol: str) -> Optional[Sign]:
        """Retrieves sign details by symbol."""
        return await self.repo.get_by_symbol(symbol.upper())

    async def seed_default_signs(self, force_refresh: bool = False) -> int:
        """Seeds or synchronizes sign language symbols in the database."""
        existing = await self.repo.get_all()
        existing_symbols = {s.symbol for s in existing}
        expected_symbols = {d["symbol"] for d in DEFAULT_SIGNS}

        if existing_symbols != expected_symbols or force_refresh:
            logger.info("Synchronizing sign vocabulary database to word definitions...")
            # Remove symbols no longer in DEFAULT_SIGNS
            for sign in existing:
                if sign.symbol not in expected_symbols:
                    await self.repo.db.delete(sign)

            # Insert new symbols or update existing ones
            for item in DEFAULT_SIGNS:
                if item["symbol"] not in existing_symbols:
                    await self.repo.create(SignCreate(**item))
                else:
                    sign = await self.repo.get_by_symbol(item["symbol"])
                    if sign:
                        sign.label = item["label"]
                        sign.category = item["category"]
                        sign.description = item["description"]
                        sign.tips = item["tips"]

            await self.repo.db.flush()
            logger.info("Vocabulary database synchronized successfully.")
            return len(expected_symbols)

        return len(existing)
