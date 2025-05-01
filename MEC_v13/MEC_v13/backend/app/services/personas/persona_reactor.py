# backend/services/persona_reactor.py

import logging
from config.security_policy import is_valid_persona
from emotion_core.fusion_engine import generate_emotionally_fused_response  # For dynamically adjusting persona

# Logging setup
logger = logging.getLogger("PersonaReactor")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("logs/persona_reactor.log")
fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(fh)

# Available personas and their emotional characteristics
personas = {
    "soothing_ally": {"tone": "calm", "energy_level": "low", "goal": "comfort_user"},
    "reflective_mentor": {"tone": "thoughtful", "energy_level": "medium", "goal": "guide_user"},
    "energetic_coach": {"tone": "motivational", "energy_level": "high", "goal": "energize_user"},
    "recovery_guardian": {"tone": "neutral", "energy_level": "medium", "goal": "ensure_safety"}
}

def generate_dynamic_persona(emotion_state: dict) -> dict:
    """
    Generates a persona dynamically based on the user's emotional state.
    """
    primary_emotion = emotion_state.get("primary_emotion", "neutral")
    intensity = emotion_state.get("intensity", 0)
    
    if primary_emotion == "sadness":
        return {
            "persona_name": "soothing_ally",
            "tone": "calm",
            "energy_level": "low",
            "goal": "comfort_user"
        }
    elif primary_emotion == "happiness":
        return {
            "persona_name": "energetic_coach",
            "tone": "motivational",
            "energy_level": "high",
            "goal": "energize_user"
        }
    elif primary_emotion == "anger":
        return {
            "persona_name": "reflective_mentor",
            "tone": "thoughtful",
            "energy_level": "medium",
            "goal": "guide_user"
        }
    else:
        # Default Persona for unknown emotion
        return {
            "persona_name": "reflective_mentor",
            "tone": "thoughtful",
            "energy_level": "medium",
            "goal": "guide_user"
        }

def react_to_symbolic(symbolic_response: dict, emotion_state: dict) -> str:
    """
    Adjusts persona dynamically based on the emotional state.
    """
    # Generate a dynamic persona based on the emotional state
    dynamic_persona = generate_dynamic_persona(emotion_state)

    # Log the chosen persona
    logger.info(f"[PersonaReactor] Reacting with dynamic persona: {dynamic_persona['persona_name']} based on emotion: {emotion_state}")

    return dynamic_persona["persona_name"]  # You can modify this to return full persona data if needed

def update_persona_state(persona: str, user_input: str, esil_state: dict) -> dict:
    """
    Updates the persona state based on user input and selected persona.
    Uses ESIL data to fine-tune the persona behavior.
    """
    logger.info(f"[PersonaReactor] Updating persona {persona} with input: {user_input} and ESIL state.")

    # Adjust persona response characteristics based on the detected emotion and intensity
    primary_emotion = esil_state.get("primary_emotion", "neutral")
    intensity = esil_state.get("intensity", 0)

    if primary_emotion == "sadness" and intensity > 0.7:
        persona = "soothing_ally"
        tone = "calm, compassionate"
        energy_level = "low"
    elif primary_emotion == "anger" and intensity > 0.7:
        persona = "recovery_guardian"
        tone = "neutral, guiding"
        energy_level = "medium"
    elif primary_emotion == "happiness" and intensity > 0.7:
        persona = "energetic_coach"
        tone = "motivational, uplifting"
        energy_level = "high"
    else:
        persona = "reflective_mentor"
        tone = "thoughtful, reflective"
        energy_level = "medium"

    # Return the updated persona state
    return {
        "persona": persona,
        "tone": tone,
        "energy_level": energy_level,
        "goal": personas[persona]["goal"]
    }

def handle_symbolic_response(user_input: str, symbolic_response: dict, esil_state: dict) -> dict:
    """
    Routes symbolic response to persona, recovery, or fusion logic.
    Integrates emotional feedback into persona generation.
    """
    logger.info(f"[Routing] Symbolic response: {symbolic_response}")

    # Generate dynamic persona from emotional context
    dynamic_persona = generate_dynamic_persona(esil_state)

    # Check if recovery or persona shift is triggered
    if symbolic_response.get("flag") == "RecoveryTriggered":
        logger.info("[Routing] Recovery Triggered")
        return update_persona_state("recovery_guardian", user_input, esil_state)
    
    # Persona decision based on the symbolic response 'goal'
    goal = symbolic_response.get("goal")
    if goal == "comfort_user":
        return update_persona_state("soothing_ally", user_input, esil_state)
    elif goal == "guide_user":
        return update_persona_state("reflective_mentor", user_input, esil_state)
    elif goal == "energize_user":
        return update_persona_state("energetic_coach", user_input, esil_state)
    else:
        # Default persona
        return update_persona_state("soothing_ally", user_input, esil_state)
