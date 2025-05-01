import pytest
from emotion_core.fusion_engine import generate_emotionally_fused_response
from core.conflict_resolver import ConflictResolver

@pytest.fixture
def symbolic_response_fixture():
    return {
        "goal": "comfort_user",
        "flag": None,
        "esil_vector": {"sadness": 0.85}
    }

@pytest.fixture
def empty_symbolic_response():
    return {}

def test_fusion_success(monkeypatch, esil_fixture, persona_fixture, symbolic_response_fixture):
    # Mock LLM response
    monkeypatch.setattr("empathy_llm.client.query_empathy_llm", lambda prompt: "I'm here for you.")
    monkeypatch.setattr("emotion_core.llm_reranker.select_best_response", lambda c, e, p: c[0])
    monkeypatch.setattr("emotion_core.modifier_engine.apply_modifiers", lambda r, l, e, options={}: r)
    monkeypatch.setattr("emotion_core.filter_engine.apply_response_filters", lambda r, d: r)

    response = generate_emotionally_fused_response(
        user_input="I'm not feeling well.",
        esil=esil_fixture,
        persona=persona_fixture,
        symbolic_response=symbolic_response_fixture
    )

    assert isinstance(response, str)
    assert "I'm here for you." in response

def test_fusion_empty_llm(monkeypatch, esil_fixture, persona_fixture, symbolic_response_fixture):
    monkeypatch.setattr("empathy_llm.client.query_empathy_llm", lambda prompt: "")
    monkeypatch.setattr("emotion_core.llm_reranker.select_best_response", lambda c, e, p: c[0] if c else "")
    monkeypatch.setattr("emotion_core.modifier_engine.apply_modifiers", lambda r, l, e, options={}: r)
    monkeypatch.setattr("emotion_core.filter_engine.apply_response_filters", lambda r, d: r)

    result = generate_emotionally_fused_response(
        user_input="I feel alone.",
        esil=esil_fixture,
        persona=persona_fixture,
        symbolic_response=symbolic_response_fixture
    )

    assert result == "[⚠️] No responses generated."

def test_conflict_resolution(monkeypatch, esil_fixture, persona_fixture, empty_symbolic_response):
    monkeypatch.setattr("empathy_llm.client.query_empathy_llm", lambda prompt: "Let's talk it out.")
    monkeypatch.setattr("emotion_core.llm_reranker.select_best_response", lambda c, e, p: c[0])
    monkeypatch.setattr("emotion_core.modifier_engine.apply_modifiers", lambda r, l, e, options={}: r)
    monkeypatch.setattr("emotion_core.filter_engine.apply_response_filters", lambda r, d: r)

    result = generate_emotionally_fused_response(
        user_input="I'm tired of trying.",
        esil=esil_fixture,
        persona=persona_fixture,
        symbolic_response=empty_symbolic_response
    )

    assert isinstance(result, str)
