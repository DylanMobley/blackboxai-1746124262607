import logging
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any
from middleware.auth_required import auth_required
from core.conflict_resolver import ConflictResolver
from core.prompt_builder import build_prompt
from core.persona_strategy_loader import get_persona_strategy
from empathy_llm.client import query_empathy_llm
from emotion_core.llm_reranker import select_best_response
from emotion_core.modifier_engine import apply_modifiers
from emotion_core.filter_engine import apply_response_filters
from backend.services.memory_store import get_memory

logger = logging.getLogger("FusionEngine")

fusion_router = APIRouter()

class PromptDebugRequest(BaseModel):
    text: str = Field(..., description="User input text")
    esil: Dict[str, Any] = Field(..., description="Emotional state vector")
    persona: Dict[str, Any] = Field(..., description="Persona strategy hints")

class PromptDebugResponse(BaseModel):
    persona_label: str
    persona_strategy: Dict[str, Any]
    generated_prompt: str

@fusion_router.post("/api/debug/prompt", response_model=PromptDebugResponse)
@auth_required
async def debug_prompt_preview(payload: PromptDebugRequest):
    persona_name = payload.persona.get("label", "soothing_ally")
    payload.persona.update(get_persona_strategy(persona_name))
    prompt = build_prompt(payload.text, payload.esil, payload.persona)

    return PromptDebugResponse(
        persona_label=persona_name,
        persona_strategy=payload.persona,
        generated_prompt=prompt
    )

def generate_emotionally_fused_response(user_input: str, esil: dict, persona: dict, symbolic_response: dict) -> str:
    logger.info("[Fusion] Initiating emotional fusion")

    persona_name = persona.get("label", "soothing_ally")
    persona.update(get_persona_strategy(persona_name))

    prompt = build_prompt(user_input, esil, persona)

    candidates = []
    for i in range(3):
        try:
            completion = query_empathy_llm(prompt)
            candidates.append(completion.strip())
        except Exception as e:
            logger.warning(f"[Fusion] Generation error: {e}")

    if not candidates:
        return "[⚠️] No responses generated."

    best = select_best_response(candidates, esil, persona)

    persona_label = persona.get("label", "soothing_ally")
    softened = apply_modifiers(best, persona_label, esil, options=persona)

    dominant_emotion = esil.get("dominant_emotion", "neutral")
    safe_output = apply_response_filters(softened, dominant_emotion)

    conflict_resolver = ConflictResolver(strategy="weighted_blend")
    unified_response = conflict_resolver.resolve(symbolic_output=symbolic_response, llm_output=safe_output)

    logger.info(f"[Fusion] Completed fusion pipeline for emotion='{dominant_emotion}'")
    return unified_response

def process_multi_modal_emotions(text_data, audio_data, visual_data):
    esil_packet = fuse_and_resolve_emotions(text_data, audio_data, visual_data)
    logger.info(f"[Fusion] Final ESIL packet after fusion: {esil_packet}")

    symbolic_response = get_symbolic_response()  # Placeholder
    return generate_emotionally_fused_response(
        user_input=text_data,
        esil=esil_packet,
        persona={},
        symbolic_response=symbolic_response
    )

def fuse_and_resolve_emotions(text_data, audio_data, visual_data):
    esil_packet = {
        "emotion_id": "some-uuid",
        "primary_emotion": text_data['primary_emotion'],
        "intensity": (audio_data['intensity'] + visual_data['intensity']) / 2,
        "confidence": max(text_data['confidence'], audio_data['confidence'], visual_data['confidence']),
        "emotion_blend": [
            text_data['primary_emotion'],
            audio_data['primary_emotion'],
            visual_data['primary_emotion']
        ],
        "timestamp_utc": "2025-04-22T18:30:00Z",
        "disagreement_score": 0.25,
        "next_action_hint": "log_to_atomspace"
    }
    return esil_packet
