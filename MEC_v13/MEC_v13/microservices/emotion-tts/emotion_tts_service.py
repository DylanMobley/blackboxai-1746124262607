# microservices/emotion-tts/emotion_tts_service.py

import os
import uuid
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from .tts_engine import generate_emotional_speech

# ─────────────────────────────────────
# Setup
# ─────────────────────────────────────
app = Flask(__name__)
CORS(app)

# Output config
AUDIO_OUTPUT_DIR = "../audio/"
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

# Logging
logger = logging.getLogger("EmotionTTSService")
logger.setLevel(logging.INFO)

# ─────────────────────────────────────
# Routes
# ─────────────────────────────────────

@app.route("/tts/generate", methods=["POST"])
def generate_tts():
    """
    POST { "text": "input text with emotion tag" }
    Returns path to generated audio file
    """
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "Text input is empty"}), 400

    try:
        output_id = str(uuid.uuid4())
        audio_path = generate_emotional_speech(text, output_id=output_id)

        # Return the public path
        public_path = f"/tts/audio/{output_id}.wav"
        logger.info(f"[✅ TTS API] Generated at {public_path}")

        return jsonify({
            "status": "completed",
            "audio_url": public_path
        })

    except Exception as e:
        logger.error("[❌ TTS GENERATION ERROR]", exc_info=True)
        return jsonify({"error": "Failed to generate audio"}), 500

@app.route("/tts/audio/<filename>")
def serve_audio(filename):
    """
    Serve generated .wav files.
    """
    return send_from_directory(AUDIO_OUTPUT_DIR, filename)

@app.route("/tts/health", methods=["GET"])
def health_check():
    """
    Simple service health ping.
    """
    return jsonify({"status": "Emotion TTS Service running 🚀"})

# ─────────────────────────────────────
# Entry
# ─────────────────────────────────────

if __name__ == "__main__":
    logger.info("🚀 Emotion TTS Service starting...")
    app.run(debug=False, host="0.0.0.0", port=5111)
