import torch
import asyncio
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "path_to_lora_model"  # Replace with actual model path or identifier

tokenizer = None
model = None

def load_lora_model():
    global tokenizer, model
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
        model.eval()
        print("LoRA model loaded successfully")
    except Exception as e:
        print(f"Failed to load LoRA model: {e}")
        tokenizer = None
        model = None
    return model

async def generate_emotional_response(model, text: str, emotion: str, context: list) -> str:
    global tokenizer
    if model is None or tokenizer is None:
        return "Model not loaded"

    # Prepare input prompt with emotion and context
    prompt = f"Emotion: {emotion}\nContext: {' '.join(context)}\nText: {text}\nResponse:"

    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = inputs.to(model.device)

    # Generate response asynchronously
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=200, do_sample=True, top_p=0.9, temperature=0.7)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract the generated part after the prompt
    response_text = response[len(prompt):].strip()
    await asyncio.sleep(0)  # Yield control to event loop
    return response_text

def prepare_input_for_lora(text: str, emotion: str, context: list):
    # This function is no longer needed with the new prompt construction
    pass
