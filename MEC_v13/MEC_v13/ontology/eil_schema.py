import jsonschema
from jsonschema import validate

# Define base EIL schema
EIL_SCHEMA = {
    "type": "object",
    "properties": {
        "primary_emotion": {"type": "string"},
        "intensity": {"type": "number"},
        "cause": {"type": "string"},
        "needs": {
            "type": "array",
            "items": {"type": "string"}
        },
        "function": {"type": "string"},
        "user_context": {"type": "string"}
    },
    "required": ["primary_emotion", "intensity", "function"]
}

def validate_eil(eil_data: dict) -> bool:
    """
    Validates the given EIL payload against the known schema.
    Throws ValidationError if invalid.
    """
    validate(instance=eil_data, schema=EIL_SCHEMA)
    return True
