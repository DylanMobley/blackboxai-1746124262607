# tests/services/test_symbolic_client.py

def test_atomese_conversion():
    from backend.services.symbolic_client import convert_esil_to_atomese

    esil = {
        "emotion_id": "uuid-123",
        "primary_emotion": "joy",
        "confidence": 0.9,
        "timestamp_utc": "2025-04-22T00:00:00Z"
    }

    atomese = convert_esil_to_atomese(esil)
    assert "PredicateNode" in atomese
    assert "ConceptNode" in atomese
    assert "joy" in atomese
