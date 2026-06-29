"""
Model Evaluation Script.

Evaluates an existing trained model on a fresh test set,
computes top-1 and top-3 accuracy, and per-class metrics.
"""

import os
import sys
import numpy as np
from sklearn.metrics import accuracy_score, top_k_accuracy_score, classification_report

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml_model.model import SignLanguageModel


def evaluate_model(
    weights_path: str = "ml_model/weights/sign_classifier.joblib",
    data_path: str = "ml_model/data/sign_landmarks_dataset.npz"
) -> None:
    """Loads model and dataset, runs comprehensive evaluation."""
    if not os.path.exists(weights_path):
        print(f"Error: weights not found at {weights_path}. Train the model first.")
        return

    if not os.path.exists(data_path):
        print(f"Error: dataset not found at {data_path}.")
        return

    model = SignLanguageModel.load(weights_path)
    data = np.load(data_path)
    X = data["X"]
    y = data["y"]
    class_names = [str(c) for c in data["class_names"]]

    # Predict probabilities
    probs = model.pipeline.predict_proba(X)
    preds = np.argmax(probs, axis=1)

    top1 = accuracy_score(y, preds)
    top3 = top_k_accuracy_score(y, probs, k=3)

    print("==========================================")
    print(f"Model Evaluation Summary")
    print(f"Top-1 Accuracy: {top1 * 100:.2f}%")
    print(f"Top-3 Accuracy: {top3 * 100:.2f}%")
    print("==========================================")
    print("\nPer-class Metrics:\n")
    print(classification_report(y, preds, target_names=class_names, digits=4))


if __name__ == "__main__":
    evaluate_model()
