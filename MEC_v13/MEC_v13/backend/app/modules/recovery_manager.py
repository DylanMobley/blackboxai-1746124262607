# backend/modules/recovery_manager.py

import logging
from backend.services.memory_store import get_memory
from empathy_llm.client import query_empathy_llm

logger = logging.getLogger("RecoveryManager")
logger.setLevel(logging.INFO)

# ─── Default Values ───────────────────────────────────
DEFAULT_INSTRUCTION = "Offer an emotionally supportive fallback when symbolic reasoning fails."

def generate_recovery(user_input: str, esil_state: dict = None) -> str:
    """
    Generate a fallback response dynamically using empathy-llm microservice.
    
    Args:
        user_input (str): Original user input.
        esil_state (dict, optional): ESIL cognitive state for emotional hinting.
    
    Returns:
        str: Generated emotional fallback response.
    """
    # Fetch persona tone
    persona_cfg = get_memory("persona_config") or {}
    tone = persona_cfg.get("tone", "gentle and supportive")

    # Fetch ESIL emotional summary
    esil_summary = esil_state.get("dominant_emotion", "unclear") if esil_state else "unclear"

    # Build recovery prompt
    recovery_prompt = f"""
You are an empathetic assistant. Your job is to create a supportive, comforting fallback message when symbolic cognition fails.

Context:
- User Emotion: {esil_summary}
- Desired Tone: {tone}

User Input:
\"\"\"{user_input}\"\"\"

Compose a brief, warm, encouraging message in response.
""".strip()

    logger.info(f"[🛟 RecoveryManager] Fallback triggered | Tone='{tone}' | Emotion='{esil_summary}'")

    try:
        fallback_response = query_empathy_llm(recovery_prompt)
        return fallback_response.strip()
    except Exception as e:
        logger.error(f"[RecoveryManager] Fallback generation failed: {e}", exc_info=True)
        return "I'm here with you. We'll find clarity together soon."

