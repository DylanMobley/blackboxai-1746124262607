# 📁 Location: mec_v13/backend/app/services/audio_video/multimodal_adapter.py

from typing import Dict, Any
from pydantic import BaseModel
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import logging

from backend.services.audio_video.audio_adapter import Wav2SkipAudioAdapter
from backend.services.audio_video.video_adapter import VideoFeatureExtractor
from backend.services.llm.dis_1_6b_client import Dis1_6bClient

logger = logging.getLogger("multimodal")
router = APIRouter()

audio_adapter = Wav2SkipAudioAdapter()
video_adapter = VideoFeatureExtractor()
dis_llm_client = Dis1_6bClient()

class AudioFeatures(BaseModel):
    pitch: float
    energy: float
    tone: str
    sentiment_score: float

class VideoFeatures(BaseModel):
    facial_expression: str
    eye_gaze: str
    movement_intensity: float
    affective_signal: str

class MultimodalEmotionPacket(BaseModel):
    audio: AudioFeatures | None = None
    video: VideoFeatures | None = None
    text_emotion: Dict[str, Any] = {}
    timestamp_utc: str

def fuse_multimodal_emotion(packet: MultimodalEmotionPacket) -> Dict[str, Any]:
    """
    Fuse audio, video, and text-derived emotion signals into a single EIL payload.
    """
    logger.info("Fusing multimodal emotion packet")

    # Extract features using adapters if raw data is present
    if packet.audio and isinstance(packet.audio, bytes):
        audio_features = audio_adapter.extract_features(packet.audio)
    else:
        audio_features = packet.audio.dict() if packet.audio else {}

    if packet.video and isinstance(packet.video, bytes):
        video_features = video_adapter.extract_features(packet.video)
    else:
        video_features = packet.video.dict() if packet.video else {}

    weights = {"text": 0.6, "audio": 0.2, "video": 0.2}
    blend = []
    disagreement_score = 0.0

    if packet.text_emotion:
        blend.append(packet.text_emotion.get("primary_emotion"))
    if audio_features:
        blend.append(audio_features.get("tone", "neutral"))
    if video_features:
        blend.append(video_features.get("affective_signal", "neutral"))

    disagreement_score = len(set(blend)) / len(blend) if blend else 0.0

    fused = {
        "emotion_id": "generated-uuid-here",
        "primary_emotion": max(set(blend), key=blend.count) if blend else "neutral",
        "intensity": packet.text_emotion.get("intensity", 0.5),
        "confidence": packet.text_emotion.get("confidence", 0.5),
        "emotion_blend": blend,
        "timestamp_utc": packet.timestamp_utc,
        "disagreement_score": round(disagreement_score, 3),
        "modality_weights": weights,
        "resolved_emotion": max(set(blend), key=blend.count) if blend else "neutral",
        "next_action_hint": "log_to_atomspace"
    }

    logger.info(f"Fused EIL: {fused}")
    return fused

@router.post("/api/emotion/multimodal")
async def fuse_multimodal_endpoint(packet: MultimodalEmotionPacket):
    fused_emotion = fuse_multimodal_emotion(packet)
    return JSONResponse(content={"fused_emotion": fused_emotion})

# ─── Optional: Utility for respond pipeline ─────────────────────────

def try_fuse_multimodal(data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if any(k in data for k in ["audio", "video"]):
            logger.info("Detected multimodal input in /respond")
            payload = MultimodalEmotionPacket(**data)
            return fuse_multimodal_emotion(payload)
    except Exception as e:
        logger.warning(f"Multimodal fusion failed, falling back: {e}")
    return None
