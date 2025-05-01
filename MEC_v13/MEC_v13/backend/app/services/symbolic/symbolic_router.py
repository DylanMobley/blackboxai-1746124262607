# symbolic_router.py

import logging
from backend.services.persona_reactor import react_to_symbolic
from backend.modules.recovery_manager import generate
from emotion_core.fusion_engine import generate_emotionally_fused_response

logger = logging.getLogger("SymbolicRouter")

def handle_symbolic_response(user_input: str, symbolic_response: dict, esil_state: dict) -> dict:
    """
    Routes symbolic response to persona, recovery, or fusion logic.
    """
    logger.info(f"[Routing] Symbolic response: {symbolic_response}")

    if symbolic_response.get("flag") == "RecoveryTriggered":
        logger.warning("[Routing] Recovery Triggered")
        response_text = generate(user_input, esil_state)
        persona = "guardian"
        goal = "restore_safety"

    else:
        persona = react_to_symbolic(symbolic_response)
        response_text = generate_emotionally_fused_response(user_input, esil_state, {"tone": persona})
        goal = symbolic_response.get("goal")

    return {
        "response": response_text,
        "persona": persona,
        "goal": goal,
        "esil_state": esil_state
    }
