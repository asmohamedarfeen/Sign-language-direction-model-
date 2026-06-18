"""
Recognition API Endpoints & WebSocket Handler.
"""

import json
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from backend.recognition.schemas.recognition import (
    GesturePredictRequest,
    GesturePredictResponse,
    ResetSentenceRequest,
    SentenceStateResponse,
    LandmarkPoint,
)
from backend.recognition.service.recognition_service import RecognitionService
from backend.recognition.dependencies import get_recognition_service
from backend.core.logging import logger

router = APIRouter(prefix="/recognition", tags=["Recognition"])


@router.post(
    "/predict",
    response_model=GesturePredictResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict sign gesture from hand landmarks"
)
async def predict_gesture(
    request: GesturePredictRequest,
    service: RecognitionService = Depends(get_recognition_service)
):
    """
    Receives 21 hand landmarks, normalizes coordinates, executes model inference,
    and updates continuous sentence transcript.
    """
    return await service.predict_gesture(request)


@router.post(
    "/reset",
    response_model=SentenceStateResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset sentence transcript for session"
)
async def reset_sentence(
    request: ResetSentenceRequest,
    service: RecognitionService = Depends(get_recognition_service)
):
    """Clears the continuous sentence builder buffer for the given session."""
    return service.reset_sentence(request.session_id)


@router.websocket("/ws/stream")
async def websocket_gesture_stream(
    websocket: WebSocket,
    service: RecognitionService = Depends(get_recognition_service)
):
    """
    High-throughput WebSocket for real-time camera streaming.
    Client sends JSON: { "landmarks": [...], "handedness": "Right", "session_id": "..." }
    Server replies with prediction, confidence, and current sentence.
    """
    await websocket.accept()
    logger.info("WebSocket client connected for real-time gesture streaming.")

    try:
        while True:
            data_text = await websocket.receive_text()
            data = json.loads(data_text)

            landmarks_raw = data.get("landmarks", [])
            if len(landmarks_raw) != 21:
                await websocket.send_json({
                    "error": True,
                    "message": f"Expected 21 landmarks, received {len(landmarks_raw)}"
                })
                continue

            landmarks = [LandmarkPoint(**pt) for pt in landmarks_raw]
            request = GesturePredictRequest(
                landmarks=landmarks,
                handedness=data.get("handedness", "Right"),
                session_id=data.get("session_id", "ws_session")
            )

            response = await service.predict_gesture(request)
            await websocket.send_text(response.model_dump_json())

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except Exception:
            pass
