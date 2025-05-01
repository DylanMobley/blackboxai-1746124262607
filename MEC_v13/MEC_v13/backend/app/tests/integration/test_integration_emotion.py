# tests/integration/test_integration_emotion.py

import pytest

@pytest.mark.asyncio
async def test_expand_emotion(client):
    payload = {"emotion": "trust"}

    response = client.post("/api/emotion/expand", json=payload)
    assert response.status_code == 200
    assert "Expanded emotion" in response.json()["status"]

@pytest.mark.asyncio
async def test_infer_emotion(client):
    payload = {
        "emotion_data": {
            "primary_emotion": "joy",
            "intensity": 0.9,
            "confidence": 0.95,
            "detected_by": ["LLM"],
            "emotion_blend": ["joy", "excitement"],
            "contextual_tags": ["achievement", "reward"],
            "timestamp_utc": "2025-04-30T12:00:00Z"
        }
    }

    response = client.post("/api/infer-emotion", json=payload)
    assert response.status_code == 200
    assert "success" in response.json()["status"]
    assert "data" in response.json()
