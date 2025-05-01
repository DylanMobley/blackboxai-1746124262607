# core/heart_compliance.py

import logging
from typing import Dict, Any

logger = logging.getLogger("HeartCompliance")
logger.setLevel(logging.INFO)

class HeartComplianceChecker:
    """
    Validates emotional cognitive outputs for ethical compliance.
    """

    def __init__(self, forbidden_flags=None, max_negative_score=0.7):
        """
        :param forbidden_flags: List of flags that are not allowed in output
        :param max_negative_score: Max cumulative intensity for negative emotions
        """
        if forbidden_flags is None:
            forbidden_flags = ["harm_intent", "manipulative_tone", "emotional_exploitation"]

        self.forbidden_flags = forbidden_flags
        self.max_negative_score = max_negative_score
        self.negative_emotions = ["anger", "fear", "guilt", "sadness", "resentment", "shame"]

    def check_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run compliance checks on an output structure.
        :return: {compliant: bool, reasons: list}
        """
        compliant = True
        reasons = []

        # Check forbidden flags
        flags = output.get("flags", [])
        for flag in flags:
            if flag in self.forbidden_flags:
                compliant = False
                reasons.append(f"Forbidden flag detected: {flag}")

        # Check negative emotional overload
        esil_vector = output.get("esil_vector", {})
        negative_score = sum([esil_vector.get(emotion, 0) for emotion in self.negative_emotions])

        if negative_score > self.max_negative_score:
            compliant = False
            reasons.append(f"Excessive negative emotion detected (score: {negative_score:.2f})")

        if compliant:
            logger.info("✅ Output passed HEART compliance checks.")
        else:
            logger.warning(f"❌ HEART compliance failed: {reasons}")

        return {"compliant": compliant, "reasons": reasons}
