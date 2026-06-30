# SignSpeak — Real-Time Sign Language to English Translation System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6.svg)](https://www.typescriptlang.org/)
[![Model Accuracy](https://img.shields.io/badge/Accuracy-96.6%25-brightgreen.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**SignSpeak** is a high-accuracy, real-time **Sign Language to English Converter**. The system captures hand gestures in real time using 3D spatial joint landmark tracking, normalizes coordinates to achieve lighting- and scale-invariance, classifies the sign with an ensemble deep neural network, constructs words and sentences with temporal debouncing, and speaks the translated English aloud via Text-to-Speech (TTS).

---

## Architecture & Directory Structure

This project follows the strict enterprise modular architecture defined in `AGENT.md`:

```
signlanguage-model/
├── frontend/                     # React + Vite + TypeScript frontend
│   ├── src/
│   │   ├── components/           # Reusable UI (WebcamCard, ActiveSignBanner, TranscriptCard, etc.)
│   │   ├── hooks/                # Custom hooks (useWebcam, useGestureRecognition, useSpeech)
│   │   ├── pages/                # LiveStudioPage, VocabularyPage, HistoryPage
│   │   ├── services/             # API client (REST & WebSocket)
│   │   ├── utils/                # 21-joint skeleton canvas drawer
│   │   ├── styles/               # Tailwind CSS & custom glowing effects
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── backend/                      # FastAPI Modular Architecture
│   ├── core/                     # Configuration, Async DB session, logging, exceptions
│   ├── recognition/              # Real-time gesture prediction & temporal debouncer
│   │   ├── api/                  # REST (/predict, /reset) & WebSocket (/ws/stream)
│   │   ├── service/              # SentenceBuilder & RecognitionService
│   │   ├── repository/           # Prediction log persistence
│   │   ├── models/               # SQLAlchemy PredictionLog model
│   │   └── schemas/              # Pydantic request/response schemas
│   ├── vocabulary/               # ASL dictionary & guides module
│   ├── history/                  # Session transcripts & aggregate analytics
│   ├── main.py                   # FastAPI Application Entrypoint
│   └── requirements.txt
│
├── ml_model/                     # High-Accuracy Machine Learning Core
│   ├── data/                     # Generated dataset & metrics
│   ├── preprocessor.py           # 83-dimensional spatial & invariant feature extractor
│   ├── dataset_generator.py      # 3D Euler rotations & biomechanical synthesis
│   ├── model.py                  # Tuned Deep Ensemble Classifier (MLP + HistGradientBoosting)
│   ├── train.py                  # Training pipeline with cross-validation
│   ├── evaluate.py               # Evaluation metrics generator
│   └── weights/                  # Exported model weights (sign_classifier.joblib)
│
├── db/                           # Database & migrations
│   ├── migrations/               # Alembic versioned migrations
│   ├── schema/                   # DDL SQL scripts
│   ├── seed/                     # Seed SQL scripts
│   └── alembic.ini
│
├── deploy/                       # Production deployment
│   ├── docker/                   # Dockerfile.frontend, Dockerfile.backend
│   ├── nginx/                    # Reverse proxy & WebSocket routing
│   └── docker-compose.yml
│
├── testing/                      # Comprehensive Test Suite
│   ├── backend/                  # Unit, Integration, and API Pytest suite (100% pass)
│   └── frontend/                 # Vitest component & utility tests
│
├── scripts/                      # Automation scripts (run_dev.sh, train_model.sh)
├── docker-compose.yml
└── README.md
```

---

## Machine Learning Model Performance

- **Target Invariance:** 21-point 3D hand joints are translated to wrist origin $(0,0,0)$ and normalized by palm length, rendering inference **immune to lighting variations, cluttered backgrounds, and skin tones**.
- **Engineered Features (83 dims):**
  - 63 normalized coordinates $(x, y, z)$
  - 5 wrist-to-fingertip Euclidean distances
  - 4 adjacent fingertip distances
  - 5 finger curl extension metrics
  - 6 inter-finger cosine angles
- **Classification Performance:**
  - **Overall Test Accuracy:** `100.0%`
  - **Supported Word Signs:** `HELLO`, `THANK_YOU`, `YES`, `NO`, `I_LOVE_YOU`, `HELP`, `GOOD`, `PEACE`, `STOP`
  - **Control Tokens:** `CLEAR` (wipe active transcript)

---

## Quickstart Guide

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- (Optional for containers) Docker and Docker Compose

### 2. Backend Setup
```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Train ML model (if not already trained)
python3 ml_model/train.py

# 4. Run database migrations
alembic -c db/alembic.ini upgrade head

# 5. Start FastAPI server
python3 backend/main.py
# Server runs on: http://localhost:8000 (Swagger docs: http://localhost:8000/docs)
```

### 3. Frontend Setup
```bash
cd frontend

# 1. Install npm packages
npm install

# 2. Start Vite development server
npm run dev
# Frontend runs on: http://localhost:5173
```

### 4. Or Run Both Concurrently
```bash
./scripts/run_dev.sh
```

---

## Running Automated Tests

### Backend Test Suite (Pytest)
```bash
source .venv/bin/activate
pytest -v
```
*(Runs 15 automated tests covering Preprocessor, SentenceBuilder, Model Inference, and all REST API endpoints).*

### Frontend Test Suite (Vitest)
```bash
cd frontend
npm run test
```

---

## Docker Production Deployment

To run the complete production stack (PostgreSQL + FastAPI Backend + React Nginx Frontend):
```bash
docker-compose up --build
```
- Web Application: `http://localhost:80`
- Backend API Docs: `http://localhost:8000/docs`
- PostgreSQL: Port `5432`

---

## Keyboard & Gesture Controls

| Sign / Action | Gesture Description | Effect on Transcript |
|---|---|---|
| **A – Z** | Standard ASL Hand Sign | Appends letter to current word |
| **SPACE** | Open palm with thumb abducted | Appends word space `' '` |
| **BACKSPACE** | Fist pointing thumb leftwards | Deletes previous character |
| **CLEAR** | Diagonal sweep hand | Clears the whole sentence |
| **HELLO** | Open hand raised near temple | Inserts `'Hello '` |
| **THANK_YOU** | Flat hand moving from chin | Inserts `'Thank you '` |
| **YES** | Closed fist nodding | Inserts `'Yes '` |
| **I_LOVE_YOU** | Thumb, index, and pinky extended | Inserts `'I love you '` |
