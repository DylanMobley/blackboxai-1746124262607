import asyncio
import logging
import zmq.asyncio
from datetime import datetime
from backend.services.symbolic_parser import parse_symbolic_response
from empathy_llm.client import query_empathy_llm

# Logging setup
logger = logging.getLogger("SymbolicClient")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("logs/symbolic_async.log")
fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(fh)

# Async ZMQ setup
ZMQ_ADDR = "tcp://127.0.0.1:5555"
TIMEOUT = 3  # seconds
RETRY_LIMIT = 2
context = zmq.asyncio.Context()

async def send_to_symbolic_engine_async(scheme_payload: str) -> dict:
    """
    Async version: Sends Atomese to symbolic engine using asyncio ZMQ.
    """
    attempt = 0
    while attempt < RETRY_LIMIT:
        try:
            socket = context.socket(zmq.REQ)
            socket.connect(ZMQ_ADDR)
            socket.setsockopt(zmq.RCVTIMEO, TIMEOUT * 1000)
            logger.info(f"[ZMQ→] Sending symbolic payload:\n{scheme_payload.strip()}")

            await socket.send_string(scheme_payload)
            response = await socket.recv_string()
            socket.close()

            logger.info(f"[ZMQ✓] Symbolic engine replied:\n{response.strip()}")
            return parse_symbolic_response(response)

        except zmq.ZMQError as e:
            logger.warning(f"[ZMQ⏱] Error on attempt {attempt+1}: {e}")
            attempt += 1
            await asyncio.sleep(0.5)
        except Exception as e:
            logger.error(f"[ZMQ💥] Unexpected error: {e}")
            break

    logger.warning("[Fallback] Switching to symbolic LLM fallback.")
    fallback = await fallback_symbolic_llm(scheme_payload)
    return {"fallback": fallback, "error": "symbolic_unreachable"}


def inject_rule(rule_atomese: str) -> str:
    """ Injects Atomese rule to the engine. """
    timestamped = f";;; Injected @ {datetime.now().isoformat()}\n{rule_atomese}"
    return timestamped  # For async version, injection should use coroutine explicitly


def convert_esil_to_atomese(esil_packet: dict) -> str:
    """ Convert ESIL packet to Atomese code for reasoning. """
    return f"""
    (EvaluationLink
        (PredicateNode "Emotion")
        (ListLink
            (ConceptNode "{esil_packet['emotion_id']}")
            (ConceptNode "{esil_packet['primary_emotion']}")
        )
    )
    (EvaluationLink
        (PredicateNode "Confidence")
        (ListLink
            (ConceptNode "{esil_packet['emotion_id']}")
            (NumberNode "{esil_packet['confidence']}")
        )
    )
    (EvaluationLink
        (PredicateNode "Timestamp")
        (ListLink
            (ConceptNode "{esil_packet['emotion_id']}")
            (StringNode "{esil_packet['timestamp_utc']}")
        )
    )
    """


async def fallback_symbolic_llm(atomese_expr: str) -> str:
    """ Uses LLM to interpret symbolic logic as fallback. """
    prompt = f"""
Interpret the following symbolic logic written in Scheme (Atomese) and explain its emotional or cognitive goal in natural language.

Atomese Expression:
"""{atomese_expr}"""

Response:
"""
    try:
        return await query_empathy_llm(prompt)
    except Exception as e:
        logger.error(f"[Fallback LLM💥] Failed to resolve Atomese: {e}")
        return "[⚠️ LLM fallback unavailable]"


# Example CLI usage
if __name__ == "__main__":
    async def test():
        test_esil = {
            "emotion_id": "test-id",
            "primary_emotion": "joy",
            "confidence": 0.91,
            "timestamp_utc": datetime.utcnow().isoformat()
        }
        atomese = convert_esil_to_atomese(test_esil)
        response = await send_to_symbolic_engine_async(atomese)
        print("[Response]", response)

    asyncio.run(test())
