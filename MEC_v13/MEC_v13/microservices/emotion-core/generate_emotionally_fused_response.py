# emotion_core/generate_emotionally_fused_response.py

import logging
from empathy_llm.client import query_empathy_llm
from symbolic.schema.atomspace_esil_map import build_atomspace_payload
from backend.services.persona_reactor import react_to_symbolic
from config.security_policy import is_valid_persona

# Logging setup
logger = logging.getLogger("EmotionallyFusedResponse")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("logs/fused_response.log")
fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(fh)

def generate_emotionally_fused_response(user_input: str, esil_state: dict, persona_data: dict) -> str:
    """
    Generates an emotionally intelligent response by integrating emotional, symbolic, and persona data.
    """
    persona = persona_data.get("tone", "soothing_ally")
    
    # Generate a symbolic response (Atomese)
    atomspace_payload = build_atomspace_payload(esil_state)
    logger.info(f"[Fused Response] Generated Atomese payload: {atomspace_payload}")

    # Generate response from the empathy-LLM model
    prompt = f"Emotion: {esil_state['vector']} | Persona: {persona} | User input: {user_input}"
    response = query_empathy_llm(prompt)

    # Apply persona adjustments (final emotional modification)
    final_response = apply_persona_tuning(response, persona)
    logger.info(f"[Fused Response] Generated final response: {final_response}")

    return final_response

def apply_persona_tuning(response: str, persona: str) -> str:
    """
    Modify the generated response based on the selected persona.
    """
    if persona == "soothing_ally":
        return f"🌸 {response} (Soothing Ally)"
    elif persona == "reflective_mentor":
        return f"💡 {response} (Reflective Mentor)"
    else:
        return f"👤 {response} (Generic Persona)"
