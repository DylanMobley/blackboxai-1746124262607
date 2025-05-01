import os
import json
import logging

logger = logging.getLogger("PersonaRegistry")
logger.setLevel(logging.INFO)

REGISTRY_PATH = os.path.join("pretrained", "personas", "persona_registry.json")

# Cache loaded registry
_persona_data = {}

def load_registry() -> dict:
    global _persona_data
    if _persona_data:
        return _persona_data

    if not os.path.exists(REGISTRY_PATH):
        logger.error(f"[✗] persona_registry.json not found at {REGISTRY_PATH}")
        return {}

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        _persona_data = json.load(f)
        logger.info(f"[✓] Loaded persona registry with {len(_persona_data)} entries")
    return _persona_data


def get_persona_by_function(func: str, goal: str = None) -> str:
    """
    Select persona that matches a given function (and optionally a goal).
    """
    registry = load_registry()

    for name, meta in registry.items():
        if func in meta.get("default_for", []):
            if goal:
                tags = meta.get("symbolic_tags", [])
                if any(goal.lower() in tag.lower() for tag in tags):
                    return name
            return name

    logger.warning(f"[!] No persona match for function='{func}', fallback used.")
    return "default_listener"


def list_persona_meta() -> list:
    """
    Returns all personas with metadata (for UI panels).
    """
    return [{"id": k, **v} for k, v in load_registry().items()]
