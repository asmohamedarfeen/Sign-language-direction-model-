"""
API End-to-End Test Suite.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from ml_model.dataset_generator import define_canonical_gestures


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_health_check(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


@pytest.mark.asyncio
async def test_vocabulary_list(async_client):
    response = await async_client.get("/api/v1/vocabulary")
    assert response.status_code == 200
    signs = response.json()
    assert len(signs) >= 10
    symbols = [s["symbol"] for s in signs]
    assert "HELLO" in symbols
    assert "THANK_YOU" in symbols
    assert "CLEAR" in symbols


@pytest.mark.asyncio
async def test_predict_endpoint(async_client):
    gestures = define_canonical_gestures()
    hand_pts = gestures["HELLO"]
    payload = {
        "landmarks": [{"x": float(p[0]), "y": float(p[1]), "z": float(p[2])} for p in hand_pts],
        "handedness": "Right",
        "session_id": "test_api_session"
    }

    response = await async_client.post("/api/v1/recognition/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_sign"] == "HELLO"
    assert data["confidence"] > 0.8
    assert "top_candidates" in data
    assert len(data["top_candidates"]) == 3


@pytest.mark.asyncio
async def test_reset_sentence_endpoint(async_client):
    response = await async_client.post("/api/v1/recognition/reset", json={"session_id": "test_api_session"})
    assert response.status_code == 200
    data = response.json()
    assert data["current_sentence"] == ""


@pytest.mark.asyncio
async def test_history_crud_and_stats(async_client):
    # 1. Create a session record
    session_payload = {
        "session_id": "integration_test_session",
        "translated_text": "HELLO THANK YOU",
        "total_gestures": 2,
        "avg_confidence": 0.98,
        "duration_seconds": 5.5
    }
    create_res = await async_client.post("/api/v1/history", json=session_payload)
    assert create_res.status_code == 201
    created = create_res.json()
    assert created["translated_text"] == "HELLO THANK YOU"
    record_id = created["id"]

    # 2. List history
    list_res = await async_client.get("/api/v1/history")
    assert list_res.status_code == 200
    items = list_res.json()
    assert any(item["id"] == record_id for item in items)

    # 3. Stats
    stats_res = await async_client.get("/api/v1/history/analytics/summary")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["total_sessions"] >= 1
    assert stats["total_words_translated"] >= 2

    # 4. Delete record
    del_res = await async_client.delete(f"/api/v1/history/{record_id}")
    assert del_res.status_code == 204
