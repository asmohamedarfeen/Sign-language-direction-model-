# Sign Language to English Converter — Architecture & Implementation Plan

**Project Version:** 1.0.0  
**Status:** Pending User Approval  
**Date:** November 2026  

---

## 1. Project Overview & Objectives

The goal of this project is to build a production-grade, highly accurate **Sign Language to English Converter** application. The system captures hand gestures in real time (via live camera or uploaded image/video), extracts spatial hand landmarks, classifies the gesture into English letters or phrases with high confidence, constructs words and sentences, and speaks them aloud via Text-to-Speech (TTS).

The project strictly follows the enterprise full-stack modular architecture defined in `AGENT.md`:
- **Frontend:** React (Vite, TypeScript, Tailwind CSS, Lucide icons, Canvas overlays)
- **Backend:** Python (FastAPI, SQLAlchemy, Alembic, Pydantic, WebSockets & REST)
- **Database:** PostgreSQL (with Alembic migrations, connection pooling, seed data)
- **ML / AI Engine:** MediaPipe 21-point 3D Landmark Extractor + Deep MLP / Random Forest Classifier with feature normalization and temporal debouncing (98%+ target accuracy)
- **Testing:** Pytest (Unit, Integration, API), Vitest/React Testing Library
- **Deployment:** Docker, Docker Compose, Nginx configuration

---

## 2. System Architecture & Project Structure

```
signlanguage-model/
├── frontend/                     # React + Vite + TypeScript frontend
│   ├── public/
│   ├── src/
│   │   ├── assets/               # Static assets, reference sign images
│   │   ├── components/           # Reusable UI components (WebcamFeed, LandmarkCanvas, TranslationCard, etc.)
│   │   ├── hooks/                # Custom hooks (useWebcam, useGestureRecognition, useSpeech)
│   │   ├── layouts/              # Main layout, Navigation, Header
│   │   ├── pages/                # RealtimeConverter, ImageUpload, History, Analytics, Vocabulary
│   │   ├── routes/               # React Router configuration
│   │   ├── services/             # API client, WebSocket client (NO business logic in UI)
│   │   ├── store/                # State management (Zustand / Context)
│   │   ├── styles/               # Tailwind CSS & global styles
│   │   ├── utils/                # Coordinate scalers, landmark drawers, formatters
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── backend/                      # FastAPI Modular Architecture
│   ├── core/                     # App-wide configuration, DB session, logging, security
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── logging.py
│   │   └── exceptions.py
│   ├── recognition/              # Feature module: Real-time & Static Sign Language Recognition
│   │   ├── api/                  # Endpoints (REST & WebSocket)
│   │   ├── service/              # Gesture prediction, temporal sequence debouncer, sentence builder
│   │   ├── repository/           # Persistence for recognition logs
│   │   ├── models/               # SQLAlchemy models (PredictionLog)
│   │   ├── schemas/              # Pydantic schemas (GestureRequest, GestureResponse, LandmarkData)
│   │   ├── routes.py
│   │   ├── dependencies.py
│   │   └── constants.py
│   ├── history/                  # Feature module: Translation history and saved transcripts
│   │   ├── api/
│   │   ├── service/
│   │   ├── repository/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes.py
│   │   └── dependencies.py
│   ├── vocabulary/               # Feature module: Sign vocabulary, guides, and reference dataset info
│   │   ├── api/
│   │   ├── service/
│   │   ├── repository/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes.py
│   │   └── dependencies.py
│   ├── main.py                   # FastAPI Application Entrypoint
│   └── requirements.txt
│
├── ml_model/                     # Machine Learning Core & Artifacts
│   ├── data/                     # Raw & processed landmark datasets
│   ├── dataset_generator.py      # Script to collect / generate landmark datasets
│   ├── train.py                  # Model training pipeline with hyperparameter tuning & cross-validation
│   ├── evaluate.py               # Generates accuracy metrics, confusion matrix, precision-recall curve
│   ├── model.py                  # Model definition (MLP / Neural Network architecture)
│   ├── preprocessor.py           # Landmark normalization (scale, origin, angle invariance)
│   └── weights/                  # Exported model weights (`sign_classifier.joblib` / `sign_classifier.onnx`)
│
├── db/                           # Database setup & migrations
│   ├── migrations/               # Alembic migration scripts
│   ├── schema/                   # DDL scripts and ER diagrams
│   ├── seed/                     # Seed data (Vocabulary signs, alphabet references)
│   └── alembic.ini
│
├── deploy/                       # Deployment configurations
│   ├── docker/                   # Dockerfiles for frontend and backend
│   │   ├── Dockerfile.frontend
│   │   └── Dockerfile.backend
│   ├── docker-compose.yml        # Multi-container orchestration (Frontend + Backend + PostgreSQL)
│   └── nginx/                    # Reverse proxy & SSL termination config
│       └── nginx.conf
│
├── testing/                      # Comprehensive Test Suite
│   ├── backend/
│   │   ├── unit/                 # Model unit tests, preprocessor tests, schema tests
│   │   ├── integration/          # Service layer & repository tests
│   │   └── api/                  # FastAPI TestClient API tests
│   └── frontend/
│       ├── unit/                 # Component and hook tests
│       └── integration/          # Translation flow tests
│
├── scripts/                      # Utility scripts (seed_db.sh, run_dev.sh, benchmark.py)
├── docs/                         # Architecture diagrams, API specs, User manuals
├── .env.example
├── README.md
└── PLANNING.md
```

---

## 3. High-Accuracy Machine Learning Model Strategy

### 3.1 Landmark-Based Spatial Modeling
Standard raw-pixel CNN models suffer from variations in lighting, background clutter, skin tone, and camera resolution. To ensure **industrial-grade accuracy (>98%)** and real-time execution (<20ms latency):
1. **MediaPipe Hands Landmark Extraction:**
   - Detects 21 3D hand landmarks ($x, y, z$ coordinates for wrists, thumb, index, middle, ring, and pinky joints).
   - Invariant to lighting, skin tone, and background.
2. **Feature Engineering & Preprocessing (`ml_model/preprocessor.py`):**
   - **Origin Translation:** Set wrist (joint 0) as reference origin $(0, 0, 0)$.
   - **Scale Invariance:** Normalize all landmark Euclidean distances relative to the palm size (distance from wrist to middle finger MCP joint).
   - **Pairwise Distance & Joint Angles:** Compute finger tip-to-palm angles and relative joint vectors. This yields a dense, highly discriminative feature vector (63 raw normalized coordinates + 20 key angle/distance metrics = 83 features).
3. **Classifier Architecture (`ml_model/model.py`):**
   - Ensemble of **Tuned Multi-Layer Perceptron (MLP)** and **Gradient Boosted Decision Forest (LightGBM/XGBoost)** or PyTorch Deep Classifier.
   - Outputs class probabilities with confidence thresholds (e.g. requires $\ge 85\%$ confidence to trigger translation).
4. **Vocabulary Coverage:**
   - **ASL Alphabet:** A, B, C, D, E, F, G, H, I, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y (static hand signs)
   - **Control Gestures:** `SPACE` (word separator), `BACKSPACE` (delete last character), `CLEAR` (reset text), `NOTHING / IDLE` (neutral hand position)
   - **Common Sign Phrases:** `HELLO`, `THANK YOU`, `YES`, `NO`, `PLEASE`, `I LOVE YOU`.

### 3.2 Real-time Sequence Debouncing & Sentence Engine
To translate continuous hand streams into natural English sentences:
- **Temporal Window Accumulator:** Retains predictions over the last 15 frames.
- **Majority Voting & Debouncing:** A letter is registered only when the gesture is stably held for $K$ consecutive frames (avoiding false positives during hand movement transitions).
- **Sentence Assembly:** Converts recognized characters into words, applies dictionary spell correction, and appends into full English sentences.
- **Audio Feedback:** Real-time Web Speech Synthesis API converts the English text to voice.

---

## 4. Backend Implementation Plan (FastAPI & PostgreSQL)

### 4.1 Modularity & Architecture
Every backend feature follows strict layer separation:
- `api/`: FastAPI route handlers, status codes, input validation.
- `service/`: Core sign translation logic, temporal buffering, speech formatting.
- `repository/`: SQLAlchemy async database queries, CRUD operations.
- `models/`: SQLAlchemy 2.0 ORM models.
- `schemas/`: Pydantic V2 schemas with strict typing and serialization.

### 4.2 Key Endpoints
- `POST /api/v1/recognition/predict`: Predict gesture from a single frame/image or landmark vector.
- `WS /api/v1/recognition/ws/stream`: High-throughput WebSocket connection for continuous frame-by-frame landmark streaming with real-time prediction feedback (<30ms round-trip).
- `GET /api/v1/vocabulary`: List all supported sign language symbols, descriptions, sample diagrams, and tips.
- `GET /api/v1/history`: Retrieve past translation sessions with timestamps, accuracy scores, and transcripts.
- `POST /api/v1/history`: Save a completed translation session.
- `GET /api/v1/analytics/stats`: Metrics on overall recognition accuracy, most frequent signs, and session statistics.
- `GET /api/v1/health`: System health and model status check.

### 4.3 Database Schema (PostgreSQL)
- **`signs` table:** ID, symbol, label, category, description, landmark_template, image_url.
- **`translation_sessions` table:** ID, session_id, translated_text, total_gestures, avg_confidence, duration_seconds, created_at.
- **`prediction_logs` table:** ID, session_id, predicted_sign, confidence, timestamp, latency_ms.

---

## 5. Frontend Implementation Plan (React + Vite + Tailwind CSS)

### 5.1 UI/UX Layout & Capabilities
- **Live Camera Studio:**
  - Full-screen or split-pane webcam interface with 60 FPS real-time MediaPipe canvas overlay drawing skeleton joints and landmarks.
  - Active Gesture Display: Large animated display showing the recognized letter/sign with confidence percentage bar.
  - Live Transcript Banner: Real-time word and sentence builder with cursor indicator.
  - Voice Controls: "Speak Sentence", "Auto TTS", "Clear", "Copy to Clipboard", "Save to History".
- **Image/Video Upload Mode:**
  - Drag-and-drop sign language photos for instant translation and landmark diagnostic breakdown.
- **Sign Language Reference Library / Dictionary:**
  - Interactive visual catalog of all supported ASL signs with 3D landmark schematics and reference images for learners.
- **Translation History & Analytics Dashboard:**
  - Searchable session log with audio playback, word counts, and confidence distributions.
- **Settings & Accessibility:**
  - Camera selection, confidence threshold slider, detection speed (FPS) tuning, dark/light theme, high-contrast mode.

---

## 6. Execution Roadmap & Milestones

| Milestone | Deliverables |
|---|---|
| **Phase 1: Planning & Approval** | Complete `PLANNING.md` specification and user sign-off. |
| **Phase 2: ML Model & Dataset** | Preprocessing pipeline, dataset generation/loading, model training with >98% accuracy, confusion matrix evaluation, exported weights (`.joblib` / `.onnx`). |
| **Phase 3: Database & Migrations** | PostgreSQL connection setup, SQLAlchemy models, Alembic migrations, initial seed data. |
| **Phase 4: FastAPI Backend** | Modular backend structure (`recognition`, `history`, `vocabulary`, `core`), REST endpoints, WebSocket streaming pipeline, unit & integration tests. |
| **Phase 5: React Frontend** | Vite + React + TypeScript setup, Tailwind styling, MediaPipe camera canvas, gesture stream hook, sentence builder, TTS, pages & components. |
| **Phase 6: Testing & QA** | Backend Pytest test suite, Frontend Vitest tests, latency and accuracy benchmarks. |
| **Phase 7: Containerization & Docs** | Dockerfiles, Docker Compose, Nginx setup, comprehensive README with setup instructions. |

---

## 7. Approval & Clarifications

Please review this plan. If you have any specific preferences on:
1. **Vocabulary scope:** Standard ASL Alphabet (A-Z) + Numbers (0-9) + Common Phrases (Hello, Thank You, Yes, No, I Love You, Help, Please).
2. **Camera mode:** Real-time browser webcam streaming with instant landmark overlay + photo upload mode.

Once you approve, we will immediately begin Phase 2 (Dataset & High-Accuracy Model Training) and proceed step-by-step through full implementation!
