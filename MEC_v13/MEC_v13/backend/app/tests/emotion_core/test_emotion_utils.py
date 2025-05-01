import pytest
from ..ontology.emotion_expander import expand_emotion
from backend.services.memory_store import set_memory, get_memory
from emotion_core.modifier_engine import apply_modifiers

# ─── Emotion Expander Tests ─────────────────────────────────────────────

def test_expand_emotion_basic():
    expanded = expand_emotion("joy")
    assert isinstance(expanded, list)
    assert "joy" in expanded

# ─── Memory Store Tests ─────────────────────────────────────────────────

def test_set_and_get_memory():
    set_memory("user_1", {"mood": "happy"})
    retrieved = get_memory("user_1")
    assert retrieved == {"mood": "happy"}

# ─── Modifier Engine Tests ──────────────────────────────────────────────

def test_apply_modifiers_no_change():
    text = "You're doing great!"
    result = apply_modifiers(text, "soothing_ally", {"dominant_emotion": "happiness"})
    assert isinstance(result, str)
    assert result.strip() != ""

# ─── Schema Validation for ESIL/Persona ────────────────────────────────
from pydantic import BaseModel, Field

class ESILSchema(BaseModel):
    primary_emotion: str
    intensity: float
    confidence: float
    timestamp_utc: str

class PersonaSchema(BaseModel):
    tone: str
    label: str = Field(default="soothing_ally")
    prompt: str = Field(default="Respond with care, empathy, and helpful intent.")

def test_valid_esil_schema():
    data = {
        "primary_emotion": "joy",
        "intensity": 0.8,
        "confidence": 0.9,
        "timestamp_utc": "2025-04-01T12:00:00Z"
    }
    model = ESILSchema(**data)
    assert model.primary_emotion == "joy"


def test_valid_persona_schema():
    data = {
        "tone": "compassionate"
    }
    model = PersonaSchema(**data)
    assert model.label == "soothing_ally"
    assert model.prompt.startswith("Respond")
