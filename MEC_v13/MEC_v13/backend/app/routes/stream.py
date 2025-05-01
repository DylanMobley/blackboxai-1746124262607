# 📁 Location: mec_v13/backend/app/routes/stream.py

from fastapi import APIRouter, Request
from fastapi.responses import EventSourceResponse
import asyncio
import json
from datetime import datetime

router = APIRouter()

# Simulated in-memory emotional state tracker (shared by reinforcement engine)
from backend.app.services.logging.reinforcement_engine import emotion_model_store

async def emotion_stream_generator():
    previous_snapshot = {}
    while True:
        await asyncio.sleep(1.5)  # Polling delay
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "emotions": emotion_model_store
        }

        # Only send if state has changed
        if payload["emotions"] != previous_snapshot:
            yield f"data: {json.dumps(payload)}\n\n"
            previous_snapshot = payload["emotions"].copy()

@router.get("/api/emotion/stream")
async def stream_emotion_state(request: Request):
    return EventSourceResponse(emotion_stream_generator())
