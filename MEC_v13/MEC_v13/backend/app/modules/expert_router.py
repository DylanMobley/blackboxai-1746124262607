import os
import json
from backend.services.memory_store import get_memory, set_memory
from backend.config.persona_registry import get_persona_by_function

DEFAULT_PERSONA = "default_listener"
PERSONA_DIR = os.path.join("pretrained", "personas")

def list_personas() -> list:
    return [f.replace(".json", "") for f in os.listdir(PERSONA_DIR) if f.endswith(".json")]

def load_persona(name: str) -> dict:
    persona_path = os.path.join(PERSONA_DIR, f"{name}.json")
    if not os.path.exists(persona_path):
        raise FileNotFoundError(f"Persona '{name}' not found.")
    
    with open(persona_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    set_memory("active_persona", name)
    set_memory("persona_config", config)
    config["name"] = name  # for consistency
    return config

def get_active_persona() -> dict:
    config = get_memory("persona_config")
    if not config:
        config = load_persona(DEFAULT_PERSONA)
    return config

def route_persona_by_function(func: str, goal: str = None) -> str:
    """
    Use persona_registry to select appropriate persona.
    """
    selected = get_persona_by_function(func, goal)
    load_persona(selected)
    return selected
