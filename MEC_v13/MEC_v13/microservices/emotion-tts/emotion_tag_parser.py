# microservices/emotion-tts/emotion_tag_parser.py

def extract_emotion_tag(text: str) -> str:
    """
    Parse text for emotion tags like [happy], [sad], [empathetic].
    If no explicit tag is found, returns [neutral] by default.
    """
    if not text:
        return "[neutral]"

    if text.startswith("[") and "]" in text:
        tag = text.split("]")[0] + "]"
        return tag.lower()

    return "[neutral]"

def strip_emotion_tag(text: str) -> str:
    """
    Removes emotion tag from text for clean TTS generation.
    """
    if text.startswith("[") and "]" in text:
        return text.split("]", 1)[1].strip()

    return text.strip()
