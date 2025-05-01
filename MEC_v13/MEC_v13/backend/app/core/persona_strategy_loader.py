import yaml
import os
from typing import Dict, Any

STRATEGY_FILE_PATH = "config/persona_rules.yaml"

class PersonaStrategyLoader:
    """
    Loads dynamic persona strategies and emotion_context rules from a YAML config.
    """

    def __init__(self, path: str = STRATEGY_FILE_PATH):
        self.path = path
        self.rules = self._load_yaml()

    def _load_yaml(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Persona strategy config not found: {self.path}")

        with open(self.path, "r") as file:
            return yaml.safe_load(file)

    def get_context(self, emotion: str, persona: str) -> str:
        """
        Fetch dynamic emotion_context logic for given emotion-persona pair.
        """
        persona_rules = self.rules.get(persona, {})
        emotion_map = persona_rules.get("emotion_context", {})
        return emotion_map.get(emotion, "Respond empathetically to the user's input.")

    def list_personas(self):
        return list(self.rules.keys())

    def list_emotions_for(self, persona: str):
        return list(self.rules.get(persona, {}).get("emotion_context", {}).keys())


# Singleton instance
persona_context_loader = PersonaStrategyLoader()
