import pytest
import asyncio
from microservices.fastapi_middleware import lora_model

@pytest.mark.asyncio
async def test_load_lora_model():
    model = lora_model.load_lora_model()
    assert model is not None, "LoRA model should be loaded"

@pytest.mark.asyncio
async def test_generate_emotional_response():
    model = lora_model.load_lora_model()
    text = "Hello, how are you?"
    emotion = "happy"
    context = ["greeting", "casual"]
    response = await lora_model.generate_emotional_response(model, text, emotion, context)
    assert isinstance(response, str)
    assert len(response) > 0
