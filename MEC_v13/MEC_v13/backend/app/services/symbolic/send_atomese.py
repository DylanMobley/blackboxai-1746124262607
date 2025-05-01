# backend/services/send_atomese.py

import logging
from tasks import send_atomese_task  # Import the Celery task

# ─── Logger Setup ───────────────────────────────────────────────
logger = logging.getLogger("SendAtomese")
logger.setLevel(logging.INFO)

def send_atomese(payload: dict) -> dict:
    """
    Sends Atomese payload to the symbolic processing system asynchronously.
    This method will now trigger the Celery task to handle the symbolic processing asynchronously.
    """
    try:
        # Call Celery task to handle Atomese sending asynchronously
        result = send_atomese_task.apply_async(args=[payload])  # Celery async task
        
        # Check the task result immediately (non-blocking, can be adjusted as needed)
        if result.ready():  
            logger.info(f"[Atomese] Payload processed successfully.")
            return result.result  # Return result if task is done
        else:
            logger.info(f"[Atomese] Task is processing asynchronously.")
            return {"status": "processing", "task_id": result.id}

    except Exception as e:
        logger.error(f"[Atomese] Failed to send Atomese payload: {e}", exc_info=True)
        return {"error": "Failed to process Atomese payload"}

