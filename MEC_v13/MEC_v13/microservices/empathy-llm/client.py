import requests
import time
import openai
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from torch import nn
from backend.model_loader.hot_swapper import ModelHotSwapper

logger = logging.getLogger(__name__)

# Configurations
EMPATHY_LLM_ENDPOINT = "http://localhost:5111/generate"
MAX_RETRIES = 3
TIMEOUT_SECONDS = 20
USE_OPENAI_FALLBACK = True
OPENAI_MODEL = "gpt-4"
OPENAI_API_KEY = "your-api-key"

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

class EmpathyLLMClient:
    def __init__(self, model_name: str = "gpt2", device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self.hot_swapper = ModelHotSwapper()
        self.model = None
        self.tokenizer = None
        self.load_model()

    def load_model(self):
        try:
            logger.info(f"Loading empathy LLM model via hot swapper: {self.model_name}")
            self.hot_swapper.load_model(
                model_name=self.model_name,
                module_path="transformers",
                loader_function="from_pretrained",
                pretrained_model_name_or_path=self.model_name
            )
            model_instance = self.hot_swapper.get_model(self.model_name)
            if model_instance:
                self.model = model_instance
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model.to(self.device)
                self.model.eval()
                logger.info("Empathy LLM model loaded successfully via hot swapper")
            else:
                logger.error("Failed to get empathy LLM model instance from hot swapper")
        except Exception as e:
            logger.error(f"Failed to load empathy LLM model via hot swapper: {e}")
            self.model = None
            self.tokenizer = None

    def sparsify_model(self, model, sparsity_level=0.8):
        for name, param in model.named_parameters():
            if "weight" in name:
                mask = torch.rand_like(param) > sparsity_level
                param.data.mul_(mask)
                logger.info(f"Pruned {name} to {sparsity_level * 100}% sparsity.")
        return model

    def query_with_sparsification(self, prompt, temperature=0.7, top_p=0.9, sparsity_level=0.8):
        sparsified_model = self.sparsify_model(self.model, sparsity_level)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = inputs.to(self.device)
        with torch.no_grad():
            outputs = sparsified_model.generate(**inputs, temperature=temperature, top_p=top_p, max_length=200)
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result

    def query(self, prompt, temperature=0.7, top_p=0.9, sparsity_level=0.8):
        if self.model is None or self.tokenizer is None:
            logger.warning("Empathy LLM model/tokenizer not loaded, returning fallback response")
            return "I'm sorry, I wasn't able to process your request right now."

        if sparsity_level:
            return self.query_with_sparsification(prompt, temperature, top_p, sparsity_level)

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(EMPATHY_LLM_ENDPOINT, json={"prompt": prompt, "temperature": temperature, "top_p": top_p}, timeout=TIMEOUT_SECONDS)
                if response.status_code == 200:
                    text = response.json().get("text", "").strip()
                    logger.info(f"[empathy-llm] Local success (attempt {attempt + 1})")
                    return text
                else:
                    logger.warning(f"[empathy-llm] HTTP {response.status_code}: {response.text}")
            except Exception as e:
                logger.error(f"[empathy-llm] Local error: {e}")
                time.sleep(1)

        if USE_OPENAI_FALLBACK and OPENAI_API_KEY:
            logger.warning("[empathy-llm] Local failed. Fallback to OpenAI...")
            try:
                completion = openai.ChatCompletion.create(
                    model=OPENAI_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    top_p=top_p
                )
                return completion["choices"][0]["message"]["content"].strip()
            except Exception as e:
                logger.error(f"[OpenAI fallback] Failure: {e}")

        logger.critical("[empathy-llm] All attempts failed. Returning fallback response.")
        return "I'm sorry, I wasn't able to process your request right now."
