import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from celery import Celery

# ─── Core Task ──────────────────────────────────────────────
from tasks import generate_emotion_video_task

# ─── Security + Middleware ──────────────────────────────────
from config.logging_config import setup_logger
from config.security_policy import (
    CLONE_API_KEY,
    ALLOWED_ORIGINS,
    MAX_TEXT_LENGTH
)
from middleware.auth_required import auth_required
from middleware.request_limiter import configure_limiter
from middleware.user_limiter import user_rate_limiter

# ─── Logger Setup ───────────────────────────────────────────
logger = setup_logger("CloneService", "logs/clone_service.log")

# ─── Flask App Init ─────────────────────────────────────────
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

app.config['VIDEO_FOLDER'] = os.path.join(os.getcwd(), 'video')
app.config['CELERY_BROKER_URL'] = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
app.config['CELERY_RESULT_BACKEND'] = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# ─── Rate Limiter Setup ─────────────────────────────────────
limiter = configure_limiter(app)

@app.before_request
def enforce_user_limits():
    return user_rate_limiter()

# ─── Request Validator ──────────────────────────────────────
def validate_request(data, require_api_key=True):
    if require_api_key and request.headers.get("X-API-KEY") != CLONE_API_KEY:
        logger.warning("🔐 Invalid API key access attempt")
        return "Unauthorized", 401
    if "text" not in data or len(data["text"]) > MAX_TEXT_LENGTH:
        logger.warning("📏 Input text too long or missing")
        return f"Text exceeds maximum ({MAX_TEXT_LENGTH})", 400
    return None

# ─── /clone-video (Direct Emotion Video Generation) ─────────
@app.route("/clone-video", methods=["POST"])
@auth_required
@limiter.limit("5 per minute")
def clone_video():
    data = request.get_json()
    validation = validate_request(data)
    if validation:
        return jsonify({"error": validation[0]}), validation[1]

    text = data["text"]
    emotion_tag = data.get("emotion", "[neutral]")
    task_id = str(uuid.uuid4())

    logger.info(f"🎬 Queuing video generation: {task_id} | Emotion: {emotion_tag}")

    try:
        generate_emotion_video_task.apply_async(args=[text, emotion_tag, task_id])
        return jsonify({
            "status": "processing",
            "task_id": task_id,
            "video_url": f"/static/video/{task_id}.mp4"
        })
    except Exception as e:
        logger.error("🚨 Failed to queue video task", exc_info=True)
        return jsonify({"error": "Queue failure"}), 500

# ─── /express (From ESIL Vector) ────────────────────────────
@app.route("/express", methods=["POST"])
@auth_required
@limiter.limit("5 per minute")
def express_from_esil():
    data = request.get_json()
    validation = validate_request(data)
    if validation:
        return jsonify({"error": validation[0]}), validation[1]

    vector = data.get("esil_vector", {})
    if not vector or not isinstance(vector, dict):
        return jsonify({"error": "Invalid ESIL vector"}), 400

    top_emotion = max(vector.items(), key=lambda x: x[1])[0]
    emotion_tag = f"[{top_emotion}]"
    text = data["text"]
    task_id = str(uuid.uuid4())

    logger.info(f"🧠 Express queue: {task_id} | Top Emotion: {top_emotion}")

    try:
        generate_emotion_video_task.apply_async(args=[text, emotion_tag, task_id])
        return jsonify({
            "status": "processing",
            "task_id": task_id,
            "inferred_emotion": top_emotion,
            "video_url": f"/static/video/{task_id}.mp4"
        })
    except Exception as e:
        logger.error("🚨 Express queue failure", exc_info=True)
        return jsonify({"error": "Queue failed"}), 500

# ─── /status & /static/video/<file> ─────────────────────────
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Emotion Clone API is online"})

@app.route("/static/video/<filename>")
def serve_video(filename):
    return send_from_directory(app.config['VIDEO_FOLDER'], filename)

# ─── Server Boot ────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(app.config['VIDEO_FOLDER'], exist_ok=True)
    logger.info("🚀 Clone Service fully operational at port 5105")
    app.run(debug=False, host="0.0.0.0", port=5105)
