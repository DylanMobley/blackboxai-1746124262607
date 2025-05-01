import pytest
from httpx import AsyncClient
from backend.api import app

@pytest.mark.asyncio
async def test_api_respond_no_auth():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/respond", json={"text": "Test"})
        assert response.status_code == 401  # Unauthorized

@pytest.mark.asyncio
async def test_api_respond_invalid_token(monkeypatch):
    async with AsyncClient(app=app, base_url="http://test") as client:
        monkeypatch.setattr("backend.api.verify_token", lambda token: False)
        headers = {"Authorization": "Bearer invalid-token"}
        response = await client.post("/api/respond", json={"text": "Test"}, headers=headers)
        assert response.status_code == 401  # Unauthorized

@pytest.mark.asyncio
async def test_api_respond_valid_token(monkeypatch):
    async with AsyncClient(app=app, base_url="http://test") as client:
        monkeypatch.setattr("backend.api.verify_token", lambda token: True)
        monkeypatch.setattr("backend.api.get_async_db", lambda: None)
        monkeypatch.setattr("backend.api.get_emotion_state", lambda data: {"primary_emotion": "happy", "intensity": 0.9, "confidence": 0.95})
        monkeypatch.setattr("backend.api.send_symbolic_request", lambda payload: {"flag": "Normal", "goal": "comfort_user"})
        monkeypatch.setattr("backend.api.generate_emotionally_fused_response", lambda text, esil, persona, symbolic: "Test response")
        monkeypatch.setattr("backend.api.react_to_symbolic", lambda symbolic: "soothing_ally")
        monkeypatch.setattr("backend.api.emotion_memory.store_emotion_state", lambda user_id, esil: None)
        monkeypatch.setattr("backend.api.set_memory", lambda key, value: None)
        monkeypatch.setattr("backend.api.get_cache", lambda key: None)
        monkeypatch.setattr("backend.api.set_cache", lambda key, value: None)

        headers = {"Authorization": "Bearer valid-token"}
        response = await client.post("/api/respond", json={"text": "Test"}, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
