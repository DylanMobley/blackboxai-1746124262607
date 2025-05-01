# core/memory_decay.py

import time
import logging
from typing import Dict, Any

logger = logging.getLogger("MemoryDecay")
logger.setLevel(logging.INFO)

class MemoryDecayManager:
    """
    Handles automatic emotional memory decay and pruning over time.
    """

    def __init__(self, half_life_seconds: int = 3600, decay_threshold: float = 0.05):
        """
        :param half_life_seconds: Time for an emotion intensity to reduce by 50%
        :param decay_threshold: If intensity falls below this, memory can be pruned
        """
        self.half_life = half_life_seconds
        self.threshold = decay_threshold
        self.last_decay_timestamps: Dict[str, float] = {}

    def apply_decay(self, esil_vector: Dict[str, float]) -> Dict[str, float]:
        """
        Apply temporal decay to an ESIL vector.
        """
        now = time.time()
        updated_vector = {}

        for emotion, intensity in esil_vector.items():
            last_timestamp = self.last_decay_timestamps.get(emotion, now)
            elapsed = now - last_timestamp

            # Calculate decay factor
            decay_factor = 0.5 ** (elapsed / self.half_life)
            new_intensity = intensity * decay_factor

            if new_intensity >= self.threshold:
                updated_vector[emotion] = new_intensity
                self.last_decay_timestamps[emotion] = now
            else:
                logger.info(f"🗑 Memory faded for '{emotion}' (below threshold)")

        return updated_vector

    def decay_and_prune(self, memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full decay and prune operation across cognitive memory dicts.
        """
        if not memory.get("vector"):
            return memory

        memory["vector"] = self.apply_decay(memory["vector"])
        return memory
