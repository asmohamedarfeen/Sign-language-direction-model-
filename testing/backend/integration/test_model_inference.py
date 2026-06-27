"""
Integration Tests for Trained Model Inference.
"""

import os
import pytest
from ml_model.model import SignLanguageModel
from ml_model.dataset_generator import define_canonical_gestures
from ml_model.preprocessor import LandmarkPreprocessor


@pytest.fixture(scope="module")
def trained_model():
    weights_path = "ml_model/weights/sign_classifier.joblib"
    assert os.path.exists(weights_path), "Model weights must exist"
    return SignLanguageModel.load(weights_path)


def test_model_loaded(trained_model):
    assert len(trained_model.class_names) == 10
    assert "HELLO" in trained_model.class_names
    assert "THANK_YOU" in trained_model.class_names
    assert "YES" in trained_model.class_names
    assert "NO" in trained_model.class_names
    assert "CLEAR" in trained_model.class_names


def test_predict_canonical_gestures(trained_model):
    gestures = define_canonical_gestures()
    test_signs = ["HELLO", "THANK_YOU", "YES", "NO", "I_LOVE_YOU", "HELP", "GOOD", "PEACE", "STOP", "CLEAR"]

    for sign in test_signs:
        landmarks = gestures[sign]
        feat = LandmarkPreprocessor.extract_features(landmarks, handedness="Right")
        pred_label, conf = trained_model.predict(feat)
        assert pred_label == sign, f"Expected {sign}, got {pred_label}"
        assert conf > 0.80, f"Confidence {conf} too low for canonical {sign}"


def test_predict_top_k(trained_model):
    gestures = define_canonical_gestures()
    feat = LandmarkPreprocessor.extract_features(gestures["HELLO"], handedness="Right")
    top_3 = trained_model.predict_top_k(feat, k=3)

    assert len(top_3) == 3
    assert top_3[0]["label"] == "HELLO"
    assert top_3[0]["confidence"] >= top_3[1]["confidence"]
