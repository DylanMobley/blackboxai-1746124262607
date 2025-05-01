import pytest
from symbolic.schema.atomspace_esil_map import build_atomspace_payload

# ─── ESIL Packet Fixtures ───────────────────────────────────────────────

@pytest.fixture
def valid_esil():
    return {
        "emotion_id": "abc-123",
        "primary_emotion": "joy",
        "intensity": 0.85,
        "confidence": 0.95,
        "timestamp_utc": "2025-05-01T14:00:00Z"
    }

@pytest.fixture
def invalid_esil():
    return {
        "primary_emotion": "joy"
        # Missing 'emotion_id', 'confidence', etc.
    }

# ─── Tests for AtomSpace Payload Construction ──────────────────────────

def test_build_atomspace_payload_valid(valid_esil):
    result = build_atomspace_payload({"esil_state": valid_esil})
    assert isinstance(result, str)
    assert "EvaluationLink" in result
    assert valid_esil["emotion_id"] in result

def test_build_atomspace_payload_invalid(invalid_esil):
    with pytest.raises(KeyError):
        build_atomspace_payload({"esil_state": invalid_esil})

# ─── Edge Case: Empty Packet ───────────────────────────────────────────

def test_empty_payload():
    with pytest.raises(KeyError):
        build_atomspace_payload({"esil_state": {}})

# ─── Edge Case: Missing ESIL Container ─────────────────────────────────

def test_missing_esil_wrapper():
    with pytest.raises(KeyError):
        build_atomspace_payload({})
