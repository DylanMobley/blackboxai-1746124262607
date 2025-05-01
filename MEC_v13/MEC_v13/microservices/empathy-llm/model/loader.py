from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from empathy_llm.config import DEFAULT_MODEL, DEVICE, MAX_TOKENS, TEMPERATURE, TOP_P

tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL)
model = AutoModelForCausalLM.from_pretrained(DEFAULT_MODEL).to(DEVICE)
llm = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if DEVICE == "cuda" else -1)

def generate_response(prompt: str) -> str:
    result = llm(prompt, max_new_tokens=MAX_TOKENS, temperature=TEMPERATURE, top_p=TOP_P)
    return result[0]["generated_text"]
