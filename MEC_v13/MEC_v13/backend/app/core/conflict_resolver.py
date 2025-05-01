# core/conflict_resolver.py

import logging
from typing import Dict, Any

logger = logging.getLogger("ConflictResolver")
logger.setLevel(logging.INFO)

class ConflictResolver:
    """
    Handles conflicts between LLM emotional generation vs Symbolic reasoning outputs.
    """

    def __init__(self, strategy: str = "weighted_blend"):
        """
        :param strategy: How to resolve conflict ("symbolic_priority", "llm_priority", "weighted_blend")
        """
        self.strategy = strategy

    def resolve(self, symbolic_output: Dict[str, Any], llm_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Harmonize two cognitive outputs.
        :param symbolic_output: Symbolic engine's decision and flags
        :param llm_output: LLM-generated empathetic response
        :return: Unified action plan
        """
        logger.info(f"🧠 Resolving conflict with strategy: {self.strategy}")

        if self.strategy == "symbolic_priority":
            return symbolic_output

        if self.strategy == "llm_priority":
            return llm_output

        if self.strategy == "weighted_blend":
            return self._blend_outputs(symbolic_output, llm_output)

        logger.warning("⚠️ Unknown conflict resolution strategy. Defaulting to symbolic.")
        return symbolic_output

    def _blend_outputs(self, symbolic_output, llm_output):
        """
        Naive blending for now: merge fields, symbolic has slight priority on flags/goals.
        """
        unified = {}

        # Merge flags / goals first
        unified["goal"] = symbolic_output.get("goal") or llm_output.get("goal")
        unified["flags"] = symbolic_output.get("flags", []) + llm_output.get("flags", [])

        # Merge emotional response second
        unified["response"] = llm_output.get("response") or symbolic_output.get("response")

        # Merge ESIL vectors if available
        symbolic_vector = symbolic_output.get("esil_vector", {})
        llm_vector = llm_output.get("esil_vector", {})

        merged_vector = {**llm_vector, **symbolic_vector}  # Symbolic overwrites LLM if both exist
        unified["esil_vector"] = merged_vector

        logger.info("🔗 Outputs merged successfully.")
        return unified

