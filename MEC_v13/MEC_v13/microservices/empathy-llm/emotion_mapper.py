import logging
from empathy_llm.client import query_empathy_llm

logger = logging.getLogger(__name__)

def map_new_emotion(emotion: str) -> dict:
    """
    Uses empathy-llm to dynamically map a new emotion into functional semantics.
    
    Args:
        emotion (str): Raw user emotion, e.g., "resentment"

    Returns:
        dict: {
            "function": "observe",
            "subtypes": [...],
            "needs": [...],
            "example": "...",
            "vector": [...]
        }
    """
    prompt = f"""
You are an emotional intelligence modeling system.

Task:
- Analyze the emotion: "{emotion}".
- Suggest a cognitive FUNCTION (e.g., observe, repair, affirm).
- List any emotional SUBTYPES related to it.
- Predict the underlying HUMAN NEEDS driving it.
- Generate a short EXAMPLE sentence showing it in use.
- Output a VECTOR embedding (5 floats between -1.0 and 1.0) that represents its psychological profile.

Respond in JSON like this:

{{
  "function": "affirm",
  "subtypes": ["trust", "loyalty"],
  "needs": ["connection", "stability"],
  "example": "I know I can depend on you when it matters most.",
  "vector": [-0.2, 0.8, 0.3, -0.1, 0.5]
}}
    """

    try:
        result = query_empathy_llm(prompt)
        parsed = eval(result.strip())  # ⚠️ Controlled internal use; if not safe, replace with json.loads
        if isinstance(parsed, dict):
            logger.info(f"[emotion_mapper] Successfully mapped emotion: {emotion}")
            return parsed
    except Exception as e:
        logger.warning(f"[emotion_mapper] Fallback mapping for emotion '{emotion}': {e}")

    # Default fallback
    return {
        "function": "observe",
        "subtypes": [],
        "needs": [],
        "example": "",
        "vector": [0.0, 0.0, 0.0, 0.0, 0.0]
    }
