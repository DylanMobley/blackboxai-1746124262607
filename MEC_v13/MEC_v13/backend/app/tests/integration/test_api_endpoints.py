import pytest
from httpx import AsyncClient
from backend.api import app

@pytest.mark.asyncio
async def test_api_root():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"status": "MEC_v13+ API is online 🧠"}

@pytest.mark.asyncio
async def test_api_health():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "OK"}

@pytest.mark.asyncio
async def test_api_respond_unauthorized():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/respond", json={"text": "Hello"})
        assert response.status_code == 401  # Unauthorized without token

@pytest.mark.asyncio
async def test_api_respond_authorized(monkeypatch):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Mock authentication and dependencies
        monkeypatch.setattr("backend.api.auth_required", lambda f: f)
        monkeypatch.setattr("backend.api.get_async_db", lambda: None)
        monkeypatch.setattr("backend.api.get_emotion_state", lambda data: {"primary_emotion": "happy", "intensity": 0.9, "confidence": 0.95})
        monkeypatch.setattr("backend.api.send_symbolic_request", lambda payload: {"flag": "Normal", "goal": "comfort_user"})
        monkeypatch.setattr("backend.api.generate_emotionally_fused_response", lambda text, esil, persona, symbolic: "Test response")
        monkeypatch.setattr("backend.api.react_to_symbolic", lambda symbolic: "soothing_ally")
        monkeypatch.setattr("backend.api.emotion_memory.store_emotion_state", lambda user_id, esil: None)
        monkeypatch.setattr("backend.api.set_memory", lambda key, value: None)
        monkeypatch.setattr("backend.api.get_cache", lambda key: None)
        monkeypatch.setattr("backend.api.set_cache", lambda key, value: None)

        headers = {"Authorization": "Bearer test-token"}
        payload = {"text": "Hello"}

        response = await client.post("/api/respond", json=payload, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["persona"] == "soothing_ally"
