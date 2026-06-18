"""
Sign Recognition Service.

Orchestrates landmark feature extraction, model prediction,
sentence building, and database logging.
"""

import time
import os
from typing import Optional, List, Dict, Any
from backend.core.config import settings
from backend.core.logging import logger
from backend.core.exceptions import ModelNotLoadedException
from backend.recognition.schemas.recognition import (
    GesturePredictRequest,
    GesturePredictResponse,
    GestureCandidate,
    SentenceStateResponse,
)
from backend.recognition.repository.prediction_log_repository import PredictionLogRepository
from backend.recognition.service.sentence_builder import SentenceBuilder
from ml_model.preprocessor import LandmarkPreprocessor
from ml_model.model import SignLanguageModel


class RecognitionService:
    """Core service for gesture recognition and translation."""

    _model: Optional[SignLanguageModel] = None
    _sentence_builder: SentenceBuilder = SentenceBuilder()

    def __init__(self, repository: PredictionLogRepository):
        self.repo = repository

    @classmethod
    def get_model(cls) -> SignLanguageModel:
        """Loads and caches the sign language model singleton."""
        if cls._model is None:
            weights_path = settings.MODEL_WEIGHTS_PATH
            if not os.path.exists(weights_path):
                logger.warning(f"Model weights not found at {weights_path}.")
                raise ModelNotLoadedException(
                    f"Model weights file not found at '{weights_path}'. Run ml_model/train.py first."
                )
            logger.info(f"Loading Sign Language model from {weights_path}...")
            cls._model = SignLanguageModel.load(weights_path)
            logger.info("Sign Language model loaded successfully.")
        return cls._model

    async def predict_gesture(
        self,
        request: GesturePredictRequest
    ) -> GesturePredictResponse:
        """
        Executes end-to-end landmark inference and sentence state update.
        """
        start_time = time.perf_counter()
        model = self.get_model()

        # 1. Feature extraction
        raw_landmarks = [
            {"x": pt.x, "y": pt.y, "z": pt.z}
            for pt in request.landmarks
        ]
        features = LandmarkPreprocessor.extract_features(
            raw_landmarks,
            handedness=request.handedness
        )

        # 2. Model inference
        candidates_raw = model.predict_top_k(features, k=3)
        top_pred = candidates_raw[0]
        predicted_sign = top_pred["label"]
        confidence = top_pred["confidence"]

        # Latency calculation
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # 3. Update temporal debouncer and sentence buffer
        session_id = request.session_id or "default_session"
        session_state = self._sentence_builder.get_or_create(session_id)
        is_stable, updated_sentence = session_state.update(predicted_sign)

        # 4. Async logging to database
        try:
            await self.repo.log_prediction(
                predicted_sign=predicted_sign,
                confidence=confidence,
                latency_ms=latency_ms,
                session_id=session_id
            )
        except Exception as e:
            logger.error(f"Failed to log prediction: {e}")

        candidates = [
            GestureCandidate(
                label=c["label"],
                confidence=c["confidence"],
                percentage=c["percentage"]
            )
            for c in candidates_raw
        ]

        return GesturePredictResponse(
            predicted_sign=predicted_sign,
            confidence=confidence,
            percentage=round(confidence * 100, 2),
            top_candidates=candidates,
            current_sentence=updated_sentence,
            latency_ms=latency_ms,
            is_stable=is_stable
        )

    def reset_sentence(self, session_id: Optional[str] = None) -> SentenceStateResponse:
        """Clears the accumulated sentence for a session."""
        sid = session_id or "default_session"
        cleared = self._sentence_builder.reset_session(sid)
        return SentenceStateResponse(
            session_id=sid,
            current_sentence=cleared,
            character_count=0,
            word_count=0
        )
