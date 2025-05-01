import os
import tempfile
import logging
from celery import Celery
from fastapi import UploadFile
from pathlib import Path

# ─── Celery Initialization ─────────────────────────────────────────
celery_app = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'))

# ─── Setup ─────────────────────────────────────────────────────────
AUDIO_OUTPUT_DIR = os.getenv('AUDIO_OUTPUT_DIR', './audio_files/')
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
logger = logging.getLogger(__name__)

# ─── Asynchronous Audio Task ───────────────────────────────────────
@celery_app.task
def process_audio_task(file_path: str) -> str:
    """
    Process and save audio file asynchronously.
    """
    try:
        audio_output_path = Path(AUDIO_OUTPUT_DIR) / Path(file_path).name
        # Assume some audio processing here (e.g., converting, normalizing)
        # For now, we simply move it to the designated directory.
        os.rename(file_path, audio_output_path)
        logger.info(f"[Audio Process] Audio saved to {audio_output_path}")
        return str(audio_output_path)
    except Exception as e:
        logger.error(f"[Audio Process Error] {str(e)}")
        raise e

# ─── Handle Audio Upload ───────────────────────────────────────────
async def handle_audio_upload(file: UploadFile) -> str:
    """
    Handle the upload of an audio file, saving it temporarily and processing it.
    """
    try:
        # Save the uploaded audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await file.read())  # Writing the uploaded content into the tmp file
            tmp_path = tmp.name
        logger.info(f"[Audio Upload] File saved temporarily at {tmp_path}")

        # Send the task to the Celery worker for processing
        result = process_audio_task.apply_async(args=[tmp_path])

        # Return the task ID for tracking
        return result.id

    except Exception as e:
        logger.error(f"[Audio Upload Error] {str(e)}")
        raise e
