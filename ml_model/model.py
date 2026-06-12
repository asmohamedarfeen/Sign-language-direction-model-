"""
Sign Language Classifier Model.

Ensemble Deep MLP & Gradient Boosted Forest for high-accuracy
ASL landmark gesture classification.
"""

from typing import List, Dict, Any, Tuple, Optional
import os
import joblib
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


class SignLanguageModel:
    """
    Production Sign Language Classifier.
    Combines feature scaling and tuned deep ensemble classification.
    """

    def __init__(self, class_names: Optional[List[str]] = None):
        self.class_names: List[str] = class_names or []
        self.pipeline: Optional[Pipeline] = None

    def build_model(self) -> Pipeline:
        """
        Builds the classifier pipeline:
        1. StandardScaler for zero mean and unit variance
        2. Deep MLP Neural Network with early stopping
        """
        mlp = MLPClassifier(
            hidden_layer_sizes=(256, 128, 64),
            activation='relu',
            solver='adam',
            alpha=0.0005,
            batch_size=64,
            learning_rate='adaptive',
            learning_rate_init=0.002,
            max_iter=300,
            early_stopping=True,
            n_iter_no_change=15,
            random_state=42
        )

        hgb = HistGradientBoostingClassifier(
            max_iter=150,
            learning_rate=0.08,
            max_leaf_nodes=31,
            random_state=42
        )

        ensemble = VotingClassifier(
            estimators=[('mlp', mlp), ('hgb', hgb)],
            voting='soft'
        )

        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', ensemble)
        ])
        return self.pipeline

    def fit(self, X: np.ndarray, y: np.ndarray, class_names: List[str]) -> "SignLanguageModel":
        """Fits the model on features X and labels y."""
        self.class_names = class_names
        if self.pipeline is None:
            self.build_model()
        self.pipeline.fit(X, y)
        return self

    def predict(self, feature_vector: np.ndarray) -> Tuple[str, float]:
        """
        Predicts gesture class and confidence percentage for a single feature vector.
        """
        if self.pipeline is None:
            raise RuntimeError("Model is not trained or loaded.")

        if feature_vector.ndim == 1:
            X = feature_vector.reshape(1, -1)
        else:
            X = feature_vector

        probs = self.pipeline.predict_proba(X)[0]
        top_idx = int(np.argmax(probs))
        confidence = float(probs[top_idx])
        label = self.class_names[top_idx] if top_idx < len(self.class_names) else "UNKNOWN"
        return label, confidence

    def predict_top_k(self, feature_vector: np.ndarray, k: int = 3) -> List[Dict[str, Any]]:
        """Returns top-k candidate predictions with confidence probabilities."""
        if self.pipeline is None:
            raise RuntimeError("Model is not trained or loaded.")

        if feature_vector.ndim == 1:
            X = feature_vector.reshape(1, -1)
        else:
            X = feature_vector

        probs = self.pipeline.predict_proba(X)[0]
        top_indices = np.argsort(probs)[::-1][:k]

        candidates = []
        for idx in top_indices:
            candidates.append({
                "label": self.class_names[idx] if idx < len(self.class_names) else "UNKNOWN",
                "confidence": float(probs[idx]),
                "percentage": round(float(probs[idx]) * 100, 2)
            })
        return candidates

    def save(self, filepath: str = "ml_model/weights/sign_classifier.joblib") -> None:
        """Saves model weights and class labels to disk."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data = {
            "pipeline": self.pipeline,
            "class_names": self.class_names
        }
        joblib.dump(data, filepath)
        print(f"Model saved successfully to {filepath}")

    @classmethod
    def load(cls, filepath: str = "ml_model/weights/sign_classifier.joblib") -> "SignLanguageModel":
        """Loads trained model weights and class metadata from disk."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model weights file not found at {filepath}")

        data = joblib.load(filepath)
        instance = cls(class_names=data["class_names"])
        instance.pipeline = data["pipeline"]
        return instance
