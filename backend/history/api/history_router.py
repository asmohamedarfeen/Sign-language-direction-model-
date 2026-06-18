"""
History API Endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from backend.history.schemas.history import SessionCreate, SessionResponse, SessionStatsResponse
from backend.history.service.history_service import HistoryService
from backend.history.dependencies import get_history_service
from backend.core.exceptions import ResourceNotFoundException

router = APIRouter(prefix="/history", tags=["History"])


@router.get(
    "",
    response_model=List[SessionResponse],
    summary="List past translation sessions",
    status_code=status.HTTP_200_OK
)
async def list_history(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: HistoryService = Depends(get_history_service)
):
    """Returns saved sign translation transcripts."""
    return await service.list_sessions(limit=limit, offset=offset)


@router.post(
    "",
    response_model=SessionResponse,
    summary="Save a translation session",
    status_code=status.HTTP_201_CREATED
)
async def create_history_record(
    session_data: SessionCreate,
    service: HistoryService = Depends(get_history_service)
):
    """Saves a completed sign language transcript and metrics."""
    return await service.record_session(session_data)


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a history session"
)
async def delete_history_record(
    session_id: int,
    service: HistoryService = Depends(get_history_service)
):
    """Removes a past translation record."""
    success = await service.remove_session(session_id)
    if not success:
        raise ResourceNotFoundException("TranslationSession", session_id)
    return None


@router.get(
    "/analytics/summary",
    response_model=SessionStatsResponse,
    summary="Get translation usage statistics",
    status_code=status.HTTP_200_OK
)
async def get_analytics_summary(
    service: HistoryService = Depends(get_history_service)
):
    """Aggregates overall translation volume, word counts, and average confidence."""
    return await service.get_summary_stats()
