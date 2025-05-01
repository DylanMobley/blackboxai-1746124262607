import pytest
from emotion_core.prompt_builder import build_prompt

# ─── Test: Basic Prompt Generation ────────────────────────────────────────

def test_build_prompt_with_emotion_context():
    user_input = "I feel overwhelmed."
    esil = {"dominant_emotion": "sadness"}
    persona = {
        "tone": "gentle",
        "prompt": "Respond gently with empathy.",
        "label": "soothing_ally"
    }

    prompt = build_prompt(user_input, esil, persona)

    assert "User Emotion: sadness" in prompt
    assert "Tone: gentle" in prompt
    assert "Respond gently with empathy." in prompt
    assert "I feel overwhelmed." in prompt

# ─── Test: Default Values ────────────────────────────────────────────────

def test_build_prompt_with_missing_fields():
    prompt = build_prompt("Hello", {}, {})

    assert "User Emotion: neutral" in prompt
    assert "Tone: compassionate and steady" in prompt
    assert "Respond with care, empathy, and helpful intent." in prompt

# ─── Test: Emotion-specific Context ──────────────────────────────────────
@pytest.mark.parametrize("emotion, expected_snippet", [
    ("sadness", "calming and empathetic"),
    ("happiness", "joy and excitement"),
    ("anger", "defuse tension")
])
def test_emotion_specific_prompt_context(emotion, expected_snippet):
    user_input = "Test message."
    esil = {"dominant_emotion": emotion}
    persona = {"tone": "test", "prompt": "instruction."}

    prompt = build_prompt(user_input, esil, persona)
    assert expected_snippet in prompt

# ─── Test: Handles Missing Emotion Field ─────────────────────────────────

def test_prompt_handles_missing_emotion():
    prompt = build_prompt("How are you?", {}, {"tone": "calm", "prompt": "Respond nicely."})
    assert "User Emotion: neutral" in prompt

# ─── Test: Handles Missing Persona Prompt ───────────────────────────────

def test_prompt_handles_missing_persona_prompt():
    esil = {"dominant_emotion": "happiness"}
    persona = {"tone": "cheerful"}  # no prompt field

    prompt = build_prompt("Let's go!", esil, persona)
    assert "Respond with care, empathy, and helpful intent." in prompt
