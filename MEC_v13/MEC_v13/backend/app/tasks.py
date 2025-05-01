import os
import logging
from celery import Celery
from backend.services.memory_store import get_memory, set_memory
from ontology.emotion_expander import expand_emotion
from symbolic.esil_analyzer import analyze_esil
from symbolic.schema.atomspace_esil_map import build_atomspace_payload
from backend.services.symbolic_client import send_atomese
from backend.services.persona_reactor import react_to_symbolic
from backend.modules.recovery_manager import generate
from emotion_core.fusion_engine import generate_emotionally_fused_response

# ─── Celery Setup ─────────────────────────────────────────────────
celery = Celery(
    "emotion_processing_tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

# ─── Logger Setup ───────────────────────────────────────────────
logger = logging.getLogger("MEC_Tasks")
logger.setLevel(logging.INFO)

@celery.task(bind=True)
def expand_emotion_task(self, emotion: str):
    """
    Expands a new emotion into the emotional function map asynchronously.
    """
    try:
        logger.info(f"[Expand] Expanding emotion: {emotion}")
        expand_emotion(emotion)
        return {"status": "success", "emotion": emotion}
    except Exception as e:
        logger.error(f"[Expand] Failed to expand emotion: {emotion} | Error: {str(e)}")
        raise self.retry(exc=e)

@celery.task(bind=True)
def process_audio_task(self, audio_path: str):
    """
    Process audio file and generate response asynchronously.
    """
    try:
        logger.info(f"[Audio] Processing audio at: {audio_path}")
        # Here, we would process the audio and return an appropriate response
        # Example: Audio transcription, emotion detection, etc.
        return {"status": "success", "audio_path": audio_path}
    except Exception as e:
        logger.error(f"[Audio] Audio processing failed for: {audio_path} | Error: {str(e)}")
        raise self.retry(exc=e)

@celery.task(bind=True)
def process_webcam_task(self, image_base64: str):
    """
    Process webcam image data and generate emotional insight asynchronously.
    """
    try:
        logger.info(f"[Webcam] Processing image data (Base64) | Length: {len(image_base64)}")
        # Here, we would decode the image, run emotion detection, etc.
        return {"status": "success", "image_base64_length": len(image_base64)}
    except Exception as e:
        logger.error(f"[Webcam] Failed to process webcam data | Error: {str(e)}")
        raise self.retry(exc=e)

@celery.task(bind=True)
def process_esil_and_generate_response(self, user_input: str, eil: dict):
    """
    Process EIL and generate a response asynchronously.
    """
    try:
        # Analyzing the Emotional Inference Language (EIL)
        esil_state = analyze_esil(eil)
        
        # Building the AtomSpace payload
        atomese_payload = build_atomspace_payload({"esil_state": esil_state})
        
        # Sending the payload to the symbolic engine
        symbolic_response = send_atomese(atomese_payload)
        
        # Reacting to the symbolic response to select the correct persona
        active_persona = react_to_symbolic(symbolic_response)
        
        # Storing results in memory
        set_memory("active_persona", active_persona)
        set_memory("esil_state", esil_state)
        set_memory("last_symbolic_state", symbolic_response)

        # Handle recovery and emotional fusion logic
        if isinstance(symbolic_response, dict) and symbolic_response.get("flag") == "RecoveryTriggered":
            logger.warning("[Recovery] Triggered")
            response = generate(user_input, esil_state)
        else:
            response = generate_emotionally_fused_response(user_input, esil_state, {"tone": active_persona})

        # Return processed response and active persona
        return {"status": "success", "response": response, "persona": active_persona}

    except Exception as e:
        logger.error(f"[ESIL] Processing failed for input: {user_input} | Error: {str(e)}")
        raise self.retry(exc=e)
