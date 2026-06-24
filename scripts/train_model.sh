#!/usr/bin/env bash
# ==========================================================
# Generate Dataset and Train Sign Language Model
# ==========================================================

set -e

source .venv/bin/activate
export PYTHONPATH=.
echo "Training Sign Language Recognition Model..."
python3 ml_model/train.py
python3 ml_model/evaluate.py
echo "Model training and evaluation complete!"
