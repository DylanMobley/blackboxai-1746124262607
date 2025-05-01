from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio
import logging
from lora_model import load_lora_model, generate_emotional_response  # LoRA integration for generating responses
from backend.model_loader.hot_swapper import ModelHotSwapper
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List

from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio
import logging
from lora_model import load_lora_model, generate_emotional_response  # LoRA integration for generating responses
from backend.model_loader.hot_swapper import ModelHotSwapper
import prometheus_client
from prometheus_client import make_asgi_app

app = FastAPI()

# Logger
logger = logging.getLogger("EmotionProcessing")
logger.setLevel(logging.INFO)

# LoRA Model Loading (using async task for efficiency)
MODEL = None
hot_swapper = ModelHotSwapper()

async def load_model():
    global MODEL
    logger.info("Loading LoRA model asynchronously via hot swapper...")
    hot_swapper.load_model(
        model_name="lora_emotion_model",
        module_path="lora_model",
        loader_function="load_lora_model"
    )
    MODEL = hot_swapper.get_model("lora_emotion_model")
    logger.info("LoRA model loaded via hot swapper.")

# Ensure model is loaded when the app starts
@app.on_event("startup")
async def startup_event():
    await load_model()

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class EmotionRequest(BaseModel):
    text: str
    emotion: str
    context: List[str]

class EmotionResponse(BaseModel):
    response: str
    emotion: str

@app.post("/process_emotion", response_model=EmotionResponse)
async def process_emotion(request: EmotionRequest, background_tasks: BackgroundTasks):
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet.")
    
    background_tasks.add_task(handle_emotion_processing, request.text, request.emotion, request.context)
    
    return {"response": "Emotion processing started, you will receive a response shortly.", "emotion": request.emotion}

async def handle_emotion_processing(text: str, emotion: str, context: List[str]):
    import time

    logger.info(f"Processing emotion: {emotion} for text: {text} with context: {context}")

    # Start timer for latency metric
    start_time = time.time()

    # Async LoRA inference - Generate emotional response based on the model
    response = await generate_emotional_response(MODEL, text, emotion, context)

    # Measure latency
    latency = time.time() - start_time
    logger.info(f"LoRA inference latency: {latency:.3f} seconds")

    # Prometheus metrics
    try:
        if not hasattr(handle_emotion_processing, "latency_metric"):
            handle_emotion_processing.latency_metric = prometheus_client.Histogram(
                "lora_inference_latency_seconds", "Latency of LoRA model inference"
            )
        handle_emotion_processing.latency_metric.observe(latency)
    except Exception as e:
        logger.error(f"Failed to record Prometheus metric: {e}")

    # Here you would call the backend or symbolic engine to further process if needed
    # For example, send the generated response to another microservice
    logger.info(f"Generated response: {response}")

    # Handle or store the final response (such as updating database or calling another service)
    # For now, just logging it
    logger.info(f"Emotion processing completed for text: {text}")
