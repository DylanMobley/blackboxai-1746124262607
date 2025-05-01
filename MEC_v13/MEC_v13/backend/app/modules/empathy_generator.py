# backend/modules/empathy_generator.py

import logging
from backend.services.memory_store import get_memory
from empathy_llm.client import query_empathy_llm

logger = logging.getLogger("EmpathyGenerator")
logger.setLevel(logging.INFO)

# ─── Defaults (Used if no persona config is found) ───────────────────────
DEFAULT_PROMPT = "You are an empathetic assistant responding to someone in distress."
DEFAULT_TONE = "gentle, supportive"

def generate_response(user_input: str, persona: str = None, esil_state: dict = None, options: dict = None) -> str:
    """
    Generate an emotionally intelligent response using the active persona configuration.
    
    Args:
        user_input (str): The user's message.
        persona (str): Active persona identifier.
        esil_state (dict): Optional ESIL vector for emotional context.
        options (dict): Additional modifier hints (e.g. style, urgency).

    Returns:
        str: Empathetic LLM-generated response.
    """
    persona_cfg = get_memory("persona_config") or {}
    tone = persona_cfg.get("tone", DEFAULT_TONE)
    prompt = persona_cfg.get("prompt", DEFAULT_PROMPT)

    emotion_context = ""
    if esil_state and "vector" in esil_state:
        top_emotion = max(esil_state["vector"], key=esil_state["vector"].get)
        emotion_context = f"The user's primary emotion is '{top_emotion}'."

    full_prompt = f"""
{prompt}
Tone: {tone}
{emotion_context}

Respond empathetically to the following message:
\"\"\"{user_input}\"\"\"

Response:
""".strip()

    try:
        result = query_empathy_llm(full_prompt)
        logger.info(f"[EmpathyGenerator] Generated empathetic response for persona '{persona or 'default'}'")
        return result.strip()
    except Exception as e:
        logger.warning(f"[EmpathyGenerator] LLM failure fallback. Error: {e}")
        return "I'm here for you. Please tell me more about how you're feeling."
