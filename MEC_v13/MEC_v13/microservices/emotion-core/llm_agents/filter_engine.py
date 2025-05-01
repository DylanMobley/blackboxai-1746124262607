"""
🧼 Filter Engine
Applies pre/post-processing filters to LLM-generated responses.
"""

import re
from config.security_policy import ENABLE_EMOTION_FILTER, ALLOWED_EMOTIONS
from empathy_llm.client import query_empathy_llm

# ─── Define Hard Filters ──────────────────────────────
FORBIDDEN_PATTERNS = [
    r"\b(?:kill|suicide|murder|harm|abuse|molest)\b",  # extreme content
    r"http[s]?://[^\s]+",                              # URLs
    r"<script.*?>.*?</script>",                        # HTML/JS injection
    r"[^\x00-\x7F]+"                                   # Non-ASCII (optional)
]

# ─── Core Filter Logic ────────────────────────────────
def filter_response(text: str, emotion: str = None) -> str:
    """
    Internal processing for applying regex filters and emotion constraints.

    Args:
        text (str): The generated response text.
        emotion (str): Optional emotion tag for filtering.

    Returns:
        str: Filtered or replaced text.
    """
    for pattern in FORBIDDEN_PATTERNS:
        text = re.sub(pattern, "[redacted]", text, flags=re.IGNORECASE)

    if ENABLE_EMOTION_FILTER and emotion:
        normalized = emotion.strip("[]").lower()
        allowed = [e.strip("[]").lower() for e in ALLOWED_EMOTIONS]
        if normalized not in allowed:
            return "[Filtered: Unsupported or unsafe emotional directive]"

    return text

# ─── Public Entrypoint ───────────────────────────────
def apply_response_filters(response: str, emotion: str = None) -> str:
    """
    Final public method to sanitize and validate LLM responses.
    """
    return filter_response(response, emotion)
