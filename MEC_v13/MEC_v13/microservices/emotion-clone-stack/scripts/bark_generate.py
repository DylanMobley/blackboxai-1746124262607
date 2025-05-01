import argparse
import os
import uuid
import logging
import soundfile as sf
from bark import generate_audio, preload_models

# ─────────────────────────────────────
# Constants
# ─────────────────────────────────────
AUDIO_OUTPUT_DIR = "../audio/"
SAMPLE_RATE = 22050

# Ensure output directory exists
os.makedirs("logs", exist_ok=True)
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────
# Logging Setup
# ─────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/worker.log"),
        logging.StreamHandler()
    ]
)

# ─────────────────────────────────────
# Preload Bark Model (global)
# ─────────────────────────────────────
logging.info("🔊 Loading Bark TTS models...")
preload_models()

# ─────────────────────────────────────
# Modular Generation Function
# ─────────────────────────────────────
def generate_audio_with_bark(text, emotion="[neutral]", output_id="sample"):
    """
    Synthesizes emotional voice using Bark TTS.
    Returns the full output .wav path.
    """
    try:
        prompt = f"{emotion} {text}".strip()
        logging.info(f"[BARK] Synthesizing: {prompt}")

        audio_array = generate_audio(prompt)
        output_path = os.path.join(AUDIO_OUTPUT_DIR, f"{output_id}.wav")
        sf.write(output_path, audio_array, SAMPLE_RATE)

        logging.info(f"[✅] Audio saved: {output_path}")
        return output_path

    except Exception as e:
        logging.error("[❌] Bark synthesis failed", exc_info=True)
        raise

# ─────────────────────────────────────
# CLI Entrypoint
# ─────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate speech using Bark TTS")
    parser.add_argument("--text", required=True, help="Text input")
    parser.add_argument("--emotion", default="[neutral]", help="Emotion tag (e.g. [sad])")
    parser.add_argument("--output", default=None, help="Optional path to save .wav")

    args = parser.parse_args()

    # Generate output_id from UUID or filename
    task_id = str(uuid.uuid4()) if not args.output else os.path.splitext(os.path.basename(args.output))[0]

    try:
        output_path = generate_audio_with_bark(
            text=args.text,
            emotion=args.emotion,
            output_id=task_id
        )
        logging.info(f"✅ Completed audio: {output_path}")
    except Exception as e:
        logging.error("Fatal Bark error in CLI", exc_info=True)
