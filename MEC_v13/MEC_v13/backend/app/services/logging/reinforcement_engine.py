# 📁 Location: mec_v13/backend/app/services/logging/reinforcement_engine.py

import redis.asyncio as redis
import asyncio
import logging
from datetime import datetime
from typing import Dict

logger = logging.getLogger("reinforcement")
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Simulated in-memory model adjustments (in production: connect to model cache or DB)
emotion_model_store: Dict[str, Dict] = {}

async def apply_reinforcement_loop():
    last_id = "$"  # Read new entries only
    logger.info("Starting reinforcement loop")

    while True:
        try:
            streams = await r.xread({"emotion_feedback": last_id}, block=5000, count=1)
            if not streams:
                continue

            for stream, entries in streams:
                for entry_id, data in entries:
                    last_id = entry_id
                    await apply_feedback(data)

        except Exception as e:
            logger.exception(f"Reinforcement loop error: {e}")
            await asyncio.sleep(2)

async def apply_feedback(entry: Dict):
    emotion_id = entry["emotion_id"]
    corrected = entry["corrected_emotion"]
    intensity = float(entry["intensity"])
    confidence = float(entry["confidence"])

    # Update in-memory state
    if emotion_id not in emotion_model_store:
        emotion_model_store[emotion_id] = {
            "primary_emotion": corrected,
            "intensity": intensity,
            "confidence": confidence,
            "revised_at": datetime.utcnow().isoformat()
        }
    else:
        # Average new feedback into existing values
        state = emotion_model_store[emotion_id]
        state["primary_emotion"] = corrected
        state["intensity"] = round((state["intensity"] + intensity) / 2, 3)
        state["confidence"] = round((state["confidence"] + confidence) / 2, 3)
        state["revised_at"] = datetime.utcnow().isoformat()

    logger.info(f"Reinforced emotion {emotion_id} → {corrected}, new state: {emotion_model_store[emotion_id]}")


# Startup hook for FastAPI

def start_reinforcement_listener():
    loop = asyncio.get_event_loop()
    loop.create_task(apply_reinforcement_loop())
