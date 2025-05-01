import os
from celery import Celery
from backend.services.worker_logger import worker_logger
from microservices.emotion-clone-stack.generate_emotion_video import generate_emotion_video

# ─── Celery Setup ─────────────────────────────────
celery = Celery(
    "emotion_clone_tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

@celery.task(bind=True)
def generate_emotion_video_task(self, text, emotion_tag, task_id):
    """
    Celery Task to create emotional avatar videos asynchronously.
    """
    worker_logger.info(f"📥 Received task: {task_id}")
    try:
        output_path = generate_emotion_video(text, emotion_tag, task_id)
        worker_logger.info(f"✅ Video completed: {output_path}")
        return {"status": "success", "path": output_path}
    except Exception as e:
        worker_logger.error(f"❌ Task failed: {e}", exc_info=True)
        raise e
