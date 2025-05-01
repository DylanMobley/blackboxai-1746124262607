
# 📁 Location: mec_v13/backend/app/api.py

import os
import logging
import datetime
from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.services.logging.reinforcement_engine import start_reinforcement_listener
from backend.app.routes.stream import router as stream_router
from backend.app.services.audio_video.multimodal_adapter import get_emotion_state

app = FastAPI()
app.include_router(stream_router)

@app.on_event("startup")
async def startup_event():
    await symbolic_pool.init_pool()
    start_reinforcement_listener()

@app.on_event("shutdown")
async def shutdown_event():
    await symbolic_pool.close_pool()

from ontology.emotion_expander import expand_emotion
from symbolic.schema.atomspace_esil_map import build_atomspace_payload
from backend.services.symbolic_client import convert_esil_to_atomese
from backend.services.persona_reactor import react_to_symbolic
from backend.services.memory_store import get_memory, set_memory
from backend.modules.emotion_memory import emotion_memory
from backend.modules.recovery_manager import generate
from emotion_core.fusion_engine import generate_emotionally_fused_response
from auth.auth_token import generate_jwt, verify_token
from backend.services.token_refresh import refresh_token
from auth.blacklist import blacklist_token
from middleware.auth_required import auth_required
from middleware.user_limiter import user_rate_limiter
from config.security_policy import ENABLE_AUTH, JWT_SECRET
from backend.async_engine import get_async_db
from backend.models import Persona, User, EmotionState

from backend.services.symbolic_client_pool import SymbolicClientPool
symbolic_pool = SymbolicClientPool()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("logs/api.log"), logging.StreamHandler()]
)

ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
if ENABLE_METRICS:
    from prometheus_flask_exporter import PrometheusMetrics
    from prometheus_client import Counter
    metrics = PrometheusMetrics(app)
    emotion_counter = Counter("eil_emotion_count_total", "ESIL vector emotion usage", ["emotion"])

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response

@app.before_request
def enforce_user_limits():
    return user_rate_limiter()

@app.get("/")
async def index():
    logging.info("⚙️ API root pinged")
    return JSONResponse(content={"status": "MEC_v13+ API is online 🧠"})

@app.get("/health")
async def health():
    return JSONResponse(content={"status": "OK"})

@app.post("/api/respond")
@auth_required
async def respond(request: Request, db: AsyncSession = Depends(get_async_db)):
    data = await request.json()
    user_input = data.get("text", "")

    cache_key = f"persona_{user_input}"
    cached_response = get_cache(cache_key)
    if cached_response:
        return JSONResponse(content=cached_response)

    esil_state = get_emotion_state(data)
    # Store emotion state in memory
    await emotion_memory.store_emotion_state(user_id, esil_state)
    user_id = 1
    active_persona = await db.execute(Persona.query.filter(Persona.user_id == user_id).first())

    if active_persona:
        logging.info(f"Using persona: {active_persona.persona_name}")
    else:
        logging.warning("No persona found for user, defaulting to 'soothing_ally'.")
        active_persona = Persona(persona_name="soothing_ally", tone="calm", energy_level="low", goal="comfort_user")
        db.add(active_persona)
        await db.commit()

    set_memory(f"persona_{user_id}", active_persona)

    atomese_payload = build_atomspace_payload({"esil_state": esil_state})
    symbolic_response = await send_symbolic_request(atomese_payload)
    active_persona_name = react_to_symbolic(symbolic_response)

    set_memory("active_persona", active_persona_name)

    if symbolic_response.get("flag") == "RecoveryTriggered":
        response = generate(user_input, esil_state)
    else:
        response = generate_emotionally_fused_response(user_input, esil_state, {"tone": active_persona_name}, symbolic_response)

    set_cache(cache_key, response)

    return JSONResponse(content={
        "persona": active_persona_name,
        "goal": symbolic_response.get("goal") if isinstance(symbolic_response, dict) else None,
        "response": response,
        "esil_state": esil_state
    })
