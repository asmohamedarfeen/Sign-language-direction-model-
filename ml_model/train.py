"""
Model Training Script.

Trains the Sign Language gesture classifier on landmark features,
computes validation metrics, and exports weights.
"""

import os
import sys
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Add workspace to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml_model.dataset_generator import generate_dataset
from ml_model.model import SignLanguageModel


def train_pipeline(
    data_path: str = "ml_model/data/sign_landmarks_dataset.npz",
    weights_path: str = "ml_model/weights/sign_classifier.joblib",
    samples_per_class: int = 400
) -> SignLanguageModel:
    """Runs the full training and evaluation pipeline."""
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Generating now...")
        X, y, class_names = generate_dataset(samples_per_class=samples_per_class, output_path=data_path)
    else:
        print(f"Loading existing dataset from {data_path}...")
        data = np.load(data_path)
        X = data["X"]
        y = data["y"]
        class_names = [str(c) for c in data["class_names"]]

    print(f"Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features, {len(class_names)} classes.")

    # Stratified Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set: {X_train.shape[0]} samples | Testing set: {X_test.shape[0]} samples")

    # Initialize and fit model
    model = SignLanguageModel()
    print("Training Deep Ensemble Classifier (MLP + HistGradientBoosting)...")
    model.fit(X_train, y_train, class_names=class_names)

    # Evaluate on test set
    y_pred = model.pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n==========================================")
    print(f" MODEL ACCURACY ON TEST SET: {acc * 100:.2f}%")
    print(f"==========================================\n")

    report = classification_report(y_test, y_pred, target_names=class_names, digits=4)
    print("Detailed Classification Report:\n", report)

    # Save trained weights
    model.save(weights_path)

    # Save summary evaluation metric to ml_model/data/metrics.txt
    metrics_path = "ml_model/data/metrics.txt"
    with open(metrics_path, "w") as f:
        f.write(f"Test Accuracy: {acc * 100:.2f}%\n")
        f.write(f"Total Samples: {len(X)}\n")
        f.write(f"Features Dimension: {X.shape[1]}\n")
        f.write(f"Classes: {len(class_names)}\n\n")
        f.write(report)
    print(f"Metrics saved to {metrics_path}")

    return model


if __name__ == "__main__":
    train_pipeline()
