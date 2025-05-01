# symbolic/esil_analyzer.py

import json
import re
from config.security_policy import is_valid_emotion

def analyze_esil(input_data):
    """
    Analyze EIL/ESIL structure.
    Accepts either full EIL JSON or raw user_input text.
    Returns normalized ESIL cognitive state dictionary.
    """

    # Case 1: Raw text input
    if isinstance(input_data, str):
        return _generate_raw_esil(input_data)

    # Case 2: Pre-structured EIL block
    if isinstance(input_data, dict):
        return _process_eil_block(input_data)

    # Fallback
    return {
        "vector": {},
        "flags": [],
        "meta": {}
    }

def _generate_raw_esil(text):
    """
    Generate a raw ESIL state from simple text input (fallback mode).
    """
    return {
        "vector": {
            "neutral": 1.0  # Assume neutral if nothing else known
        },
        "flags": ["raw_input"],
        "meta": {
            "source": "text",
            "length": len(text),
        }
    }

def _process_eil_block(eil_block):
    """
    Parse full EIL JSON and extract emotion vector dynamically.
    """
    emotions = eil_block.get("emotions", [])
    meta = eil_block.get("meta", {})

    vector = {}

    for emotion_item in emotions:
        label = emotion_item.get("label", "").strip()
        score = emotion_item.get("score", 0)

        if not label or not is_valid_emotion(label):
            continue  # Skip invalid formats

        # Strip brackets and normalize
        clean_label = label.strip("[]").lower()

        vector[clean_label] = score

    return {
        "vector": vector,
        "flags": ["structured_input"],
        "meta": meta
    }
