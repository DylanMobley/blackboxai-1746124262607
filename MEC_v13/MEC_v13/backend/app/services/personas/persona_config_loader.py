# backend/services/persona_config_loader.py

import os
import json
import logging

logger = logging.getLogger("PersonaConfigLoader")
logger.setLevel(logging.INFO)

# 🔗 Central persona config file
PERSONA_CONFIG_JSON = "backend/config/persona_configs.json"

def load_persona_config(persona: str) -> dict:
    """
    Load dynamic persona configuration (tone, style, prompts) by persona name.

    Args:
        persona (str): Name of the active persona.

    Returns:
        dict: Persona configuration including tone and generation hints.
    """
    if not os.path.exists(PERSONA_CONFIG_JSON):
        logger.warning(f"[⚠️] Persona config file missing at {PERSONA_CONFIG_JSON}")
        return {}

    with open(PERSONA_CONFIG_JSON, "r") as f:
        try:
            config_map = json.load(f)
        except json.JSONDecodeError:
            logger.error("[❌] Invalid JSON structure in persona config.")
            return {}

    persona_key = persona.lower()

    if persona_key not in config_map:
        logger.warning(f"[❓] Persona '{persona_key}' not found, using default.")
        return {}

    logger.info(f"[✅] Loaded config for persona: '{persona_key}'")
    return config_map.get(persona_key, {})

def list_available_personas() -> list:
    """
    List all persona keys available.

    Returns:
        list: List of persona names.
    """
    if not os.path.exists(PERSONA_CONFIG_JSON):
        return []

    with open(PERSONA_CONFIG_JSON, "r") as f:
        try:
            config_map = json.load(f)
        except json.JSONDecodeError:
            return []

    return list(config_map.keys())
