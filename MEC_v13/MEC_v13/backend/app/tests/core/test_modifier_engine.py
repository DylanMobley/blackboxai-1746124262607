import pytest
from ..emotion_core.modifier_engine import apply_modifiers

# ─── Fixtures ───

@pytest.fixture
def example_persona():
    return {
        "label": "soothing_ally",
        "tone": "calm",
        "energy_level": "low",
        "goal": "comfort_user"
    }

@pytest.fixture
def example_esil():
    return {
        "dominant_emotion": "sadness",
        "intensity": 0.8,
        "confidence": 0.9
    }

# ─── Tests ───

def test_modifier_preserves_meaning(example_persona, example_esil):
    original_response = "I'm here for you during this tough time."
    modified = apply_modifiers(original_response, "soothing_ally", example_esil, options=example_persona)

    assert isinstance(modified, str)
    assert len(modified) > 0
    assert "I'm here for you" in modified

def test_modifier_handles_missing_persona():
    response = apply_modifiers("Stay strong.", None, {"dominant_emotion": "anger"}, options={})
    assert isinstance(response, str)
    assert "Stay strong" in response

def test_modifier_with_different_personas(example_esil):
    variants = [
        ("reflective_mentor", "Take a moment to consider this..."),
        ("energetic_coach", "You've got this!"),
        ("recovery_guardian", "Safety is our top priority.")
    ]

    for label, phrase in variants:
        output = apply_modifiers(phrase, label, example_esil, options={"label": label})
        assert phrase in output
        assert isinstance(output, str)
        assert len(output) > 0
