"""
Vocabulary Module Dependencies.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import get_db
from backend.vocabulary.repository.sign_repository import SignRepository
from backend.vocabulary.service.sign_service import SignService


async def get_sign_repository(
    db: AsyncSession = Depends(get_db)
) -> SignRepository:
    """Dependency providing SignRepository instance."""
    return SignRepository(db)


async def get_sign_service(
    repo: SignRepository = Depends(get_sign_repository)
) -> SignService:
    """Dependency providing SignService instance."""
    return SignService(repo)
