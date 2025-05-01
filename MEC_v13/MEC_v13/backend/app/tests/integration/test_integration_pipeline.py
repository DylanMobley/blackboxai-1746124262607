# tests/integration/test_integration_pipeline.py

import pytest
from httpx import AsyncClient
from backend.api import app

@pytest.mark.asyncio
async def test_full_emotion_pipeline(monkeypatch):
    async with AsyncClient(app=app, base_url="http://test") as client:

        monkeypatch.setattr("empathy_llm.client.query_empathy_llm", lambda prompt: "You are not alone.")
        monkeypatch.setattr("emotion_core.llm_reranker.select_best_response", lambda c, e, p: c[0])
        monkeypatch.setattr("emotion_core.modifier_engine.apply_modifiers", lambda r, l, e, options={}: r)
        monkeypatch.setattr("emotion_core.filter_engine.apply_response_filters", lambda r, d: r)

        payload = {
            "text": "I feel lost and hopeless",
            "eil": {
                "primary_emotion": "sadness",
                "intensity": 0.85,
                "confidence": 0.9,
                "timestamp_utc": "2025-04-30T00:00:00Z"
            }
        }

        headers = {"Authorization": "Bearer test-token"}  # if auth_required stubbed in tests

        response = await client.post("/api/respond", json=payload, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "persona" in data
        assert data["persona"] in ["soothing_ally", "reflective_mentor", "recovery_guardian"]


# tests/integration/test_invalid_env.py
import subprocess
import pytest

def test_invalid_env_keys(tmp_path):
    invalid_env = tmp_path / ".env"
    invalid_env.write_text("INVALID_KEY=value\n")

    result = subprocess.run(
        ["python", "scripts/validate_env.py", str(invalid_env)],
        capture_output=True,
        text=True
    )

    assert result.returncode != 0
    assert "ValidationError" in result.stderr
