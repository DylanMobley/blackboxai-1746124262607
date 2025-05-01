import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from core.prompt_builder import build_prompt
from api.debug.fusion_engine import fusion_router

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(fusion_router)
    return app

@pytest.mark.asyncio
async def test_debug_prompt_preview(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/debug/prompt",
            headers={"Authorization": "Bearer test_token"},
            json={
                "text": "I feel overwhelmed by everything lately.",
                "esil": {"dominant_emotion": "sadness"},
                "persona": {"label": "soothing_ally"}
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "generated_prompt" in data
        assert data["persona_label"] == "soothing_ally"
        assert "tone" in data["persona_strategy"]
