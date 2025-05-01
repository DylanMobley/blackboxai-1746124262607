# emotion_core/llm_reranker.py

import logging
from empathy_llm.client import query_empathy_llm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def select_best_response(candidates, esil=None, persona=None):
    """
    Selects the best emotional response from a list of candidates using LLM-driven judgment.

    Args:
        candidates (list of str): LLM-generated response options.
        esil (dict, optional): Emotional state info for contextual alignment.
        persona (str, optional): Persona influencing tone or intent.

    Returns:
        str: The best-matching response.
    """

    if not candidates:
        logger.warning("[llm_reranker] No candidates provided, returning fallback.")
        return "I'm here for you."

    prompt = build_reranker_prompt(candidates, esil, persona)

    try:
        best_response = query_empathy_llm(prompt, temperature=0.5, top_p=0.8)
        logger.info("[llm_reranker] Successfully reranked responses.")
        return best_response.strip()
    except Exception as e:
        logger.error(f"[llm_reranker] Reranking failed: {e}, falling back to first candidate.")
        return candidates[0]

def build_reranker_prompt(candidates, esil=None, persona=None):
    """
    Constructs a reranker prompt to determine the best emotional fit.

    Args:
        candidates (list of str): Responses to evaluate.
        esil (dict, optional): Emotional cues.
        persona (str, optional): Persona context.

    Returns:
        str: Prompt for the LLM reranker.
    """
    dominant_emotion = esil.get("dominant_emotion") if esil else "empathetic"

    options = "\n\n".join([f"Option {idx+1}: {c}" for idx, c in enumerate(candidates)])
    persona_hint = f"with the persona '{persona}'" if persona else "in an empathetic style"

    prompt = f"""
You are an emotionally intelligent assistant tasked with selecting the best response based on emotional appropriateness, clarity, and supportiveness.

The user's dominant emotion is '{dominant_emotion}'.

Choose the best response {persona_hint}:

{options}

Reply ONLY with the full best Option (no commentary):
    """.strip()

    return prompt
