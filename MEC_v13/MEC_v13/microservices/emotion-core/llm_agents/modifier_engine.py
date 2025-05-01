import logging
from empathy_llm.client import query_empathy_llm

logger = logging.getLogger(__name__)

def apply_modifiers(raw_text, persona, esil_state=None, options=None):
    """
    Dynamically modifies emotional tone, phrasing, and format using an LLM prompt.

    Args:
        raw_text (str): The raw LLM response.
        persona (str): Selected persona style.
        esil_state (dict): Optional ESIL vector state for top emotion.
        options (dict): Optional modifiers like 'style', 'intent', etc.

    Returns:
        str: Transformed response styled with persona and emotional cues.
    """
    prompt = build_modifier_prompt(raw_text, persona, esil_state, options)

    try:
        modified_text = query_empathy_llm(prompt)
        logger.info(f"[modifier_engine] ✅ Modified with persona '{persona}'")
        return modified_text.strip()
    except Exception as e:
        logger.warning(f"[modifier_engine] ⚠️ LLM failed, fallback to raw text | {e}")
        return raw_text

def build_modifier_prompt(text, persona, esil_state=None, options=None):
    """
    Constructs a rich instruction prompt to stylize output.

    Args:
        text (str): Raw AI response text.
        persona (str): Persona to apply.
        esil_state (dict): ESIL emotion vector.
        options (dict): Additional styling hints.

    Returns:
        str: Prompt for LLM refinement.
    """
    top_emotion = ""
    if esil_state and "vector" in esil_state:
        top_emotion = max(esil_state["vector"], key=esil_state["vector"].get)

    emotion_hint = f"The user's dominant emotion is '{top_emotion}'." if top_emotion else ""

    persona_hint = {
        "soothing_ally": "Rewrite the message with a warm, compassionate tone that soothes the user.",
        "assertive_mirror": "Express the message with honesty and confident, respectful directness.",
        "insightful_mentor": "Deliver the message with insightful emotional clarity and guidance.",
        "empathic_guide": "Rephrase using nurturing language and heartfelt empathy."
    }.get(persona, f"Rewrite using the emotional style of '{persona}'.")

    intent_hint = options.get("intent", "") if options else ""
    style_hint = options.get("style", "") if options else ""

    return f"""
You are an emotionally intelligent assistant that modifies tone, clarity, and empathy.

{emotion_hint}
{persona_hint}
{intent_hint}
{style_hint}

ORIGINAL RESPONSE:
\"\"\"{text}\"\"\"

MODIFIED RESPONSE:
""".strip()
