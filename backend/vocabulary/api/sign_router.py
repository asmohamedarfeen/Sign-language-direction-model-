"""
Vocabulary API Endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from backend.vocabulary.schemas.sign import SignResponse
from backend.vocabulary.service.sign_service import SignService
from backend.vocabulary.dependencies import get_sign_service
from backend.core.exceptions import ResourceNotFoundException

router = APIRouter(prefix="/vocabulary", tags=["Vocabulary"])


@router.get(
    "",
    response_model=List[SignResponse],
    summary="List all supported signs",
    status_code=status.HTTP_200_OK
)
async def list_signs(
    category: Optional[str] = Query(None, description="Filter by alphabet, word, or control"),
    service: SignService = Depends(get_sign_service)
):
    """Retrieves all sign language vocabulary symbols and guides."""
    return await service.list_signs(category=category)


@router.get(
    "/{symbol}",
    response_model=SignResponse,
    summary="Get sign details by symbol",
    status_code=status.HTTP_200_OK
)
async def get_sign(
    symbol: str,
    service: SignService = Depends(get_sign_service)
):
    """Retrieves specific details and instructions for a gesture symbol."""
    sign = await service.get_sign(symbol)
    if not sign:
        raise ResourceNotFoundException("Sign", symbol)
    return sign
