# backend/services/emotion_expander.py

import os
import json
import logging
from empathy_llm.client import query_empathy_llm
from config.security_policy import is_valid_emotion

logger = logging.getLogger("EmotionExpander")
logger.setLevel(logging.INFO)

# 🔗 Central emotion function map store
EMOTION_FUNCTIONS_JSON = "ontology/emotional_functions.json"

def expand_emotion(emotion: str) -> None:
    """
    Dynamically expand and register a new emotion into the emotional_functions map.
    """
    if not is_valid_emotion(emotion):
        raise ValueError(f"Invalid emotion format: {emotion}")

    emotion_key = emotion.strip("[]").lower()

    # Load current map or init
    emotion_map = {}
    if os.path.exists(EMOTION_FUNCTIONS_JSON):
        with open(EMOTION_FUNCTIONS_JSON, "r") as f:
            emotion_map = json.load(f)

    if emotion_key in emotion_map:
        logger.info(f"[⚡] Emotion '{emotion_key}' already mapped.")
        return

    logger.info(f"[🔍] Expanding unknown emotion: '{emotion_key}'")

    # Build LLM prompt
    prompt = f"""
    You are an emotional cognition engine. Provide a structured emotional mapping for the emotion '{emotion_key}'.
    
    Format your response as JSON with these fields:
    - function: (string) primary function like "connect", "protect", "observe", "release"
    - subtypes: (list) any emotional subtypes or variations
    - needs: (list) what unmet needs this emotion may reflect
    - example: (string) a sentence demonstrating this emotion in use
    - vector: (optional list of floats) a conceptual embedding

    Only return valid JSON.
    """.strip()

    try:
        response = query_empathy_llm(prompt)
        mapping = json.loads(response)
        assert isinstance(mapping, dict)
    except Exception as e:
        logger.warning(f"[❌] Emotion LLM mapping failed: {e}")
        mapping = {
            "function": "observe",
            "subtypes": [],
            "needs": [],
            "example": "I'm feeling something I can't quite name.",
            "vector": []
        }

    # Update map
    emotion_map[emotion_key] = mapping

    with open(EMOTION_FUNCTIONS_JSON, "w") as f:
        json.dump(emotion_map, f, indent=2)

    logger.info(f"[✅] Emotion '{emotion_key}' added to function map.")
