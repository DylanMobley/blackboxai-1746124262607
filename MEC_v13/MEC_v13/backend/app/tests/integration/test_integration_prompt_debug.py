import pytest

def test_prompt_debug_endpoint(client):
    payload = {
        "user_input": "I feel overwhelmed",
        "persona": {
            "tone": "gentle",
            "prompt": "Respond gently with empathy.",
            "label": "soothing_ally"
        },
        "esil": {
            "dominant_emotion": "sadness",
            "emotion_id": "debug-id-1",
            "intensity": 0.75,
            "confidence": 0.95,
            "timestamp_utc": "2025-04-30T10:00:00Z"
        }
    }

    response = client.post("/api/debug/prompt", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prompt" in data
    assert "sadness" in data["prompt"]
    assert "gentle" in data["prompt"]
