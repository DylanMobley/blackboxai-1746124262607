# microservices/emotion-tts/tts_engine.py

import os
import uuid
import logging
import soundfile as sf
from bark import generate_audio, preload_models
from .emotion_tag_parser import extract_emotion_tag, strip_emotion_tag

# ─────────────────────────────────────
# Configs
# ─────────────────────────────────────
OUTPUT_DIR = "../audio/"
SAMPLE_RATE = 22050

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────
# Logging
# ─────────────────────────────────────
logger = logging.getLogger("EmotionTTS")
logger.setLevel(logging.INFO)

# ─────────────────────────────────────
# Initialization
# ─────────────────────────────────────
preload_models()

# ─────────────────────────────────────
# Core TTS Engine
# ─────────────────────────────────────
def generate_emotional_speech(text: str, output_id: str = None) -> str:
    """
    Generate speech audio file from emotional text input.
    :param text: Text with embedded emotion tag [happy], [sad], etc.
    :param output_id: Optional UUID or identifier
    :return: Path to generated .wav file
    """
    if output_id is None:
        output_id = str(uuid.uuid4())

    emotion_tag = extract_emotion_tag(text)
    clean_text = strip_emotion_tag(text)

    prompt = f"{emotion_tag} {clean_text}".strip()

    logger.info(f"[🎙️ EmotionTTS] Generating speech for: {prompt}")

    try:
        audio_array = generate_audio(prompt)
        output_path = os.path.join(OUTPUT_DIR, f"{output_id}.wav")
        sf.write(output_path, audio_array, SAMPLE_RATE)

        logger.info(f"[✅ TTS] Saved output: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"[❌ TTS ERROR] Failed to generate speech", exc_info=True)
        raise e
