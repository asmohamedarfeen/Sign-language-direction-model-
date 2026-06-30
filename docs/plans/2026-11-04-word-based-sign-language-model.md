# Implementation Plan: Word-Based Sign Language Model & Direction Calibration

## Overview
Transition the sign language recognition system from single-letter fingerspelling (A–Z) to whole-word conversational sign classification. Calibrate 3D landmark orientations to match MediaPipe camera coordinates directly, retrain the classifier, and update backend services and frontend UI.

---

## Tasks

### Task 1: Re-align Canonical Pose Coordinates & Replace Alphabet with Word Vocabulary
- **Files**: `ml_model/dataset_generator.py`, `ml_model/preprocessor.py`
- Re-align base anatomical coordinates to match MediaPipe's real-time coordinate system ($Y$ negative upwards, wrist at origin $(0, 0, 0)$).
- Define distinct canonical poses for words: `HELLO`, `THANK_YOU`, `YES`, `NO`, `I_LOVE_YOU`, `HELP`, `GOOD`, `PEACE`, `STOP`, and control token `CLEAR`.
- Remove all single-letter (A–Y) alphabet gestures.

### Task 2: Retrain Classifier & Export Model Weights
- **Files**: `ml_model/train.py`, `ml_model/evaluate.py`, `ml_model/weights/sign_classifier.joblib`
- Run the training pipeline to generate the augmented word dataset.
- Train the deep ensemble classifier (HistGradientBoosting + MLP).
- Verify validation accuracy > 95% and export model weights.

### Task 3: Update Backend Constants, Sentence Builder, and Vocabulary Service
- **Files**:
  - `backend/recognition/constants.py`
  - `backend/recognition/service/sentence_builder.py`
  - `backend/vocabulary/constants.py`
  - `backend/vocabulary/service/sign_service.py`
- Configure word signs as first-class citizens in `SentenceBuilder` (spacing, punctuation, clearing).
- Update default vocabulary list with definitions and tips for each word.
- Update database seeding so the SQLite table reflects the new word vocabulary.

### Task 4: Update Backend Test Suite
- **Files**:
  - `testing/backend/test_preprocessor.py`
  - `testing/backend/test_sentence_builder.py`
  - `testing/backend/test_model.py`
  - `testing/backend/test_api.py`
- Update unit and API tests to assert word predictions (`HELLO`, `THANK_YOU`, etc.) instead of letters.
- Run `pytest -v` to ensure 100% pass rate.

### Task 5: Update Frontend Vocabulary View & Tests
- **Files**:
  - `frontend/src/pages/VocabularyPage.tsx`
  - `frontend/src/pages/LiveStudioPage.tsx`
  - `frontend/src/tests/` (if any vitest tests touch vocabulary)
- Update vocabulary filters, card badges, and prompt recommendations for whole words.
- Run `npm test` in `frontend/`.

### Task 6: Final Verification
- Run backend test suite.
- Run frontend build & test suite.
- Verify health check and model loading.
