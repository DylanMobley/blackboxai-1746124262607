# backend/services/symbolic_client.py

import zmq
import time
import logging
from empathy_llm.client import query_empathy_llm

logger = logging.getLogger("SymbolicClient")
logger.setLevel(logging.INFO)

# ─── ZMQ Configuration ─────────────────────────────
ZMQ_ADDR = "tcp://127.0.0.1:5556"
TIMEOUT_MS = 3000
RETRY_LIMIT = 2

# ─── ZMQ Context ───────────────────────────────────
context = zmq.Context()

# ─── Primary Request Logic ─────────────────────────
def send_atomese(atomese_code: str) -> str:
    """
    Sends Scheme/Atomese code to symbolic engine via ZMQ.
    Returns: string response or fallback.
    """
    retries = 0
    response = None

    while retries < RETRY_LIMIT:
        try:
            socket = context.socket(zmq.REQ)
            socket.connect(ZMQ_ADDR)
            socket.setsockopt(zmq.RCVTIMEO, TIMEOUT_MS)
            socket.send_string(atomese_code)
            response = socket.recv_string()
            logger.info(f"[↔️] Symbolic ZMQ response: {response}")
            socket.close()
            break
        except zmq.error.Again:
            logger.warning(f"[⏱️] Timeout on symbolic engine ({retries+1}/{RETRY_LIMIT})")
            retries += 1
            socket.close()
            time.sleep(0.25)
        except Exception as e:
            logger.error(f"[💥] Symbolic engine failure: {e}")
            socket.close()
            break

    if not response:
        logger.warning("[🧠] Falling back to LLM-generated symbolic explanation.")
        response = fallback_symbolic_llm(atomese_code)

    return response or "[⚠️] Symbolic system unavailable."

# ─── ZMQ Action Injector ───────────────────────────
def inject_rule(scheme_block: str) -> str:
    """
    Sends a cognitive rule to AtomSpace via `(cog-execute!)`.
    """
    wrapped = f"(cog-execute! '{scheme_block})"
    logger.info(f"[📤] Injecting symbolic rule:\n{wrapped}")
    return send_atomese(wrapped)

# ─── ZMQ Read Query ────────────────────────────────
def query_expression(scheme_expr: str) -> str:
    """
    Runs symbolic queries without changing AtomSpace state.
    """
    logger.info(f"[🔍] Querying symbolic engine:\n{scheme_expr}")
    return send_atomese(scheme_expr)

# ─── LLM Fallback Resolver (Emergency) ─────────────
def fallback_symbolic_llm(atomese_expr: str) -> str:
    """
    If the symbolic engine is unreachable, ask empathy-llm to interpret the intent.
    """
    prompt = f"""
Interpret the following symbolic logic written in Scheme (Atomese) and explain its emotional or cognitive goal in natural language.

Atomese Expression:
\"\"\"{atomese_expr}\"\"\"

Response:"""

    try:
        return query_empathy_llm(prompt)
    except Exception as e:
        logger.error(f"[🧪] Symbolic LLM fallback failed: {e}")
        return "[LLM fallback unavailable]"
