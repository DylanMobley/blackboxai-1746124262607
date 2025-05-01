import argparse
import subprocess
import os
import uuid
import logging
from pathlib import Path

# Logging Setup
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/worker.log"),
        logging.StreamHandler()
    ]
)

# Paths
AVATAR_IMAGE = "../avatars/base_photo.jpg"
AUDIO_OUTPUT = "../audio/output.wav"

# Fetch environment variable or default to 'bark'
TTS_MODEL = os.getenv("TTS_MODEL", "bark").lower()

# Logging the selected TTS model
logging.info(f"Using TTS model: {TTS_MODEL}")

# Function to generate voice based on TTS system
def generate_voice(text, emotion_tag):
    if TTS_MODEL == "bark":
        logging.info("🔊 Generating audio with Bark...")
        # Replace with actual Bark generation code
        subprocess.run(["python3", "scripts/bark_generate.py", "--text", text, "--emotion", emotion_tag, "--output", AUDIO_OUTPUT])
    elif TTS_MODEL == "dis16b":
        logging.info("🔊 Generating audio with Dis 1.6b...")
        # Replace with actual Dis 1.6b generation code
        subprocess.run(["python3", "scripts/dis16b_generate.py", "--text", text, "--emotion", emotion_tag, "--output", AUDIO_OUTPUT])
    else:
        logging.error(f"❌ Unsupported TTS model: {TTS_MODEL}")
        raise ValueError(f"Unsupported TTS model: {TTS_MODEL}")

# Function to generate face video
def generate_face_video(output_path):
    logging.info(f"🎬 Generating face video at {output_path}...")
    # Video generation logic (for example using SadTalker)
    subprocess.run(["python3", SADTALKER_SCRIPT, "--input", AVATAR_IMAGE, "--audio", AUDIO_OUTPUT, "--output", output_path])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate avatar video")
    parser.add_argument("--text", required=True)
    parser.add_argument("--emotion", default="[neutral]")
    parser.add_argument("--output", help="Output path (.mp4)")

    args = parser.parse_args()

    # Fallback UUID output
    output_path = args.output or f"../video/{str(uuid.uuid4())}.mp4"

    try:
        generate_voice(args.text, args.emotion)
        generate_face_video(output_path)
        logging.info(f"✅ Done: {output_path}")
    except Exception as e:
        logging.error("Unhandled error", exc_info=True)
