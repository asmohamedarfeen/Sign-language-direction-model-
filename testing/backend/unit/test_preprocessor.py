"""
Unit Tests for Landmark Preprocessor.
"""

import pytest
import numpy as np
from ml_model.preprocessor import LandmarkPreprocessor


def test_landmarks_to_array_from_dicts():
    landmarks_dict = [{"x": float(i), "y": float(i * 2), "z": float(i * 0.1)} for i in range(21)]
    arr = LandmarkPreprocessor.landmarks_to_array(landmarks_dict)
    assert arr.shape == (21, 3)
    assert arr[0, 0] == 0.0
    assert arr[1, 1] == 2.0


def test_normalize_landmarks_wrist_origin():
    raw = np.ones((21, 3), dtype=np.float32) * 5.0
    # Set middle MCP far away
    raw[9] = [5.0, 7.0, 5.0]
    norm = LandmarkPreprocessor.normalize_landmarks(raw)
    # Wrist (index 0) must be exactly at (0, 0, 0)
    assert np.allclose(norm[0], [0.0, 0.0, 0.0])


def test_extract_features_shape():
    raw_landmarks = [{"x": 0.1 * i, "y": 0.2 * i, "z": 0.01 * i} for i in range(21)]
    # Ensure middle finger MCP is non-zero
    raw_landmarks[9]["y"] = 1.0

    features = LandmarkPreprocessor.extract_features(raw_landmarks, handedness="Right")
    assert isinstance(features, np.ndarray)
    assert features.shape == (83,)
    assert features.dtype == np.float32


def test_invalid_landmarks_length():
    short_landmarks = [{"x": 0.1, "y": 0.2, "z": 0.0} for _ in range(10)]
    with pytest.raises(ValueError):
        LandmarkPreprocessor.extract_features(short_landmarks)
