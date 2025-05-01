import argparse
import os
import uuid
import subprocess
import logging

# ─────────────────────────────────────
# Constants
# ─────────────────────────────────────
AVATAR_DEFAULT = "../avatars/base_photo.jpg"
VIDEO_OUTPUT_DIR = "../video/"
os.makedirs("logs", exist_ok=True)
os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)

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
# Core Function (Importable)
# ─────────────────────────────────────
def generate_video(audio_path, output_id="sample", avatar_path=AVATAR_DEFAULT, still=True, enhancer="gfpgan"):
    """
    Generates talking head video using SadTalker.
    Returns the full path to the generated .mp4 video.
    """
    output_name = output_id.replace(".mp4", "")
    output_path = os.path.join(VIDEO_OUTPUT_DIR, f"{output_name}.mp4")

    command = [
        "python", "inference.py",
        "--driven_audio", audio_path,
        "--source_image", avatar_path,
        "--result_dir", VIDEO_OUTPUT_DIR,
        "--output_name", output_name,
    ]

    if still:
        command.append("--still")
    if enhancer:
        command.extend(["--enhancer", enhancer])

    try:
        logging.info(f"[SADTALKER] Generating: {output_name}")
        logging.info(f"[CMD] {' '.join(command)}")
        subprocess.run(command, check=True)
        logging.info(f"✅ SadTalker completed: {output_path}")
        return output_path

    except subprocess.CalledProcessError as e:
        logging.error("❌ SadTalker subprocess failed", exc_info=True)
        raise

    except Exception as e:
        logging.error("❌ Unexpected SadTalker error", exc_info=True)
        raise

# ─────────────────────────────────────
# CLI Entrypoint
# ─────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SadTalker CLI - Animate avatar with emotional voice")
    parser.add_argument("--driven_audio", required=True, help="Path to .wav audio file")
    parser.add_argument("--source_image", default=AVATAR_DEFAULT, help="Path to avatar photo")
    parser.add_argument("--output_name", default=str(uuid.uuid4()), help="Unique video output ID")
    parser.add_argument("--still", action="store_true", help="Use still face mode")
    parser.add_argument("--enhancer", default="gfpgan", help="Enhancer model (optional)")

    args = parser.parse_args()

    try:
        generate_video(
            audio_path=args.driven_audio,
            output_id=args.output_name,
            avatar_path=args.source_image,
            still=args.still,
            enhancer=args.enhancer
        )
    except Exception as e:
        logging.error("Fatal error in SadTalker CLI", exc_info=True)
