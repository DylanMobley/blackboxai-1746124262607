# tests/integration/test_pipeline_symbolic_llm.py

import pytest
from fastapi.testclient import TestClient
from backend.api import app

client = TestClient(app)

@pytest.mark.integration
def test_pipeline_response_success(monkeypatch):
    """
    Full pipeline: ESIL -> Symbolic -> Persona -> LLM -> Final Response
    """
    # Simulate LLM and Symbolic success
    monkeypatch.setattr("empathy_llm.client.query_empathy_llm", lambda prompt: "Empathic response here.")
    monkeypatch.setattr("emotion_core.llm_reranker.select_best_response", lambda c, e, p: c[0])
    monkeypatch.setattr("emotion_core.modifier_engine.apply_modifiers", lambda r, l, e, options={}: r)
    monkeypatch.setattr("emotion_core.filter_engine.apply_response_filters", lambda r, d: r)

    payload = {
        "text": "I'm really frustrated with everything.",
        "eil": {"dominant_emotion": "anger"}
    }

    response = client.post("/api/respond", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["persona"] in ["reflective_mentor", "soothing_ally"]
    assert "esil_state" in data

@pytest.mark.integration
def test_pipeline_recovery_trigger(monkeypatch):
    """
    Simulate RecoveryTriggered symbolic response and verify fallback.
    """
    monkeypatch.setattr("backend.services.symbolic_client_pool.symbolic_pool.send", lambda a: {"flag": "RecoveryTriggered"})
    monkeypatch.setattr("backend.modules.recovery_manager.generate", lambda u, e: "Fallback recovery response.")

    response = client.post("/api/respond", json={
        "text": "I'm not safe.",
        "eil": {"dominant_emotion": "fear"}
    })

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "Fallback recovery response."
    assert data["persona"] == "recovery_guardian"

@pytest.mark.integration
def test_pipeline_symbolic_fallback(monkeypatch):
    """
    Simulate symbolic failure and test fallback to default persona.
    """
    monkeypatch.setattr("backend.services.symbolic_client_pool.symbolic_pool.send", lambda a: {})
    monkeypatch.setattr("empathy_llm.client.query_empathy_llm", lambda prompt: "Safe output.")
    monkeypatch.setattr("emotion_core.llm_reranker.select_best_response", lambda c, e, p: c[0])
    monkeypatch.setattr("emotion_core.modifier_engine.apply_modifiers", lambda r, l, e, options={}: r)
    monkeypatch.setattr("emotion_core.filter_engine.apply_response_filters", lambda r, d: r)

    response = client.post("/api/respond", json={
        "text": "What's the point?",
        "eil": {"dominant_emotion": "sadness"}
    })

    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["persona"] in ["soothing_ally"]
