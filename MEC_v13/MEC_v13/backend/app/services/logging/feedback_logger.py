# 📁 Location: mec_v13/backend/app/services/feedback_logger.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from datetime import datetime
import redis.asyncio as redis
import uuid

router = APIRouter()

# Initialize Redis connection (production-ready: move config to settings)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

class FeedbackPayload(BaseModel):
    emotion_id: str = Field(..., description="Original emotion state UUID")
    corrected_emotion: str = Field(..., description="Corrected primary emotion")
    intensity: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str = Field(..., description="Human correction rationale")
    user_id: str = Field(..., description="Reviewer ID")
    tags: list[str] = Field(default_factory=list)

@router.post("/emotion/feedback")
async def submit_feedback(payload: FeedbackPayload, request: Request):
    try:
        log_entry = {
            "log_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "ip": request.client.host,
            **payload.dict()
        }

        await r.xadd("emotion_feedback", log_entry)
        return {"status": "logged", "log_id": log_entry["log_id"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
