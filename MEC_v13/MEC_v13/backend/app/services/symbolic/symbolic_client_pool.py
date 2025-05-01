import asyncio
import logging
import zmq
import zmq.asyncio
from contextlib import asynccontextmanager
from prometheus_client import Counter, start_http_server, generate_latest, CONTENT_TYPE_LATEST
from empathy_llm.client import query_empathy_llm
from fastapi import FastAPI, Response

logger = logging.getLogger("SymbolicClientPool")
logger.setLevel(logging.INFO)

ZMQ_ADDRESS = "tcp://localhost:5555"
RETRY_LIMIT = 3
RETRY_DELAY = 0.5  # seconds
TIMEOUT_MS = 3000

# Prometheus metrics
symbolic_timeouts = Counter("symbolic_timeouts_total", "Number of symbolic engine timeouts")
symbolic_errors = Counter("symbolic_errors_total", "Number of symbolic engine errors")
symbolic_retries = Counter("symbolic_retries_total", "Total retries for symbolic engine communication")
symbolic_fallbacks = Counter("symbolic_fallback_total", "Fallbacks to LLM when symbolic engine fails")
symbolic_requests = Counter("symbolic_requests_total", "Total symbolic requests sent")

class SymbolicZMQPool:
    def __init__(self, zmq_address=ZMQ_ADDRESS, pool_size=4, timeout_ms=TIMEOUT_MS):
        self.zmq_address = zmq_address
        self.pool_size = pool_size
        self.timeout_ms = timeout_ms
        self.context = zmq.asyncio.Context()
        self.sockets = asyncio.Queue()
        self._initialized = False

    async def init_pool(self):
        logger.info(f"[ZMQ] Initializing symbolic socket pool ({self.pool_size})")
        for _ in range(self.pool_size):
            socket = self.context.socket(zmq.REQ)
            socket.setsockopt(zmq.RCVTIMEO, self.timeout_ms)
            socket.connect(self.zmq_address)
            await self.sockets.put(socket)
        self._initialized = True

    async def close_pool(self):
        logger.info("[ZMQ] Closing symbolic socket pool")
        while not self.sockets.empty():
            socket = await self.sockets.get()
            socket.close()
        self.context.term()

    @asynccontextmanager
    async def get_socket(self):
        socket = await self.sockets.get()
        try:
            yield socket
        finally:
            await self.sockets.put(socket)

    async def send(self, atomese_code: str) -> str:
        if not self._initialized:
            raise RuntimeError("ZMQ pool is not initialized")

        retries = 0
        symbolic_requests.inc()

        while retries < RETRY_LIMIT:
            async with self.get_socket() as socket:
                try:
                    await socket.send_string(atomese_code)
                    response = await socket.recv_string()
                    logger.info(f"[ZMQ] Received symbolic response: {response}")
                    return response
                except zmq.error.Again:
                    symbolic_timeouts.inc()
                    symbolic_retries.inc()
                    logger.warning(f"[ZMQ] Timeout {retries + 1}/{RETRY_LIMIT}: No response from symbolic engine.")
                except zmq.ZMQError as e:
                    symbolic_errors.inc()
                    logger.error(f"[ZMQ] Engine communication failure: {e}")
                    break
                except Exception as e:
                    symbolic_errors.inc()
                    logger.exception(f"[ZMQ] Unexpected error: {e}")
                    break

                await asyncio.sleep(RETRY_DELAY * (retries + 1))
                retries += 1

        logger.error("[ZMQ] Symbolic engine unreachable after retries. Falling back to LLM.")
        symbolic_fallbacks.inc()
        return self._fallback_to_llm(atomese_code)

    def _fallback_to_llm(self, atomese_expr: str) -> str:
        prompt = f'''
Interpret the following symbolic logic written in Scheme (Atomese) and explain its emotional or cognitive goal in natural language.

Atomese Expression:
"""{atomese_expr}"""

Response:
'''
        try:
            return query_empathy_llm(prompt)
        except Exception as e:
            logger.error(f"[LLM Fallback] Failed to interpret Atomese: {e}")
            return "[LLM fallback unavailable]"


def start_metrics_server(port=9102):
    """
    Starts Prometheus HTTP server for metrics scraping.
    """
    import threading
    threading.Thread(target=start_http_server, args=(port,), daemon=True).start()
    logger.info(f"[📊] Prometheus metrics server running on port {port}/metrics")

# Global pool instance
symbolic_pool = SymbolicZMQPool()

# FastAPI app (for Prometheus endpoint)
metrics_app = FastAPI()

@metrics_app.on_event("startup")
async def startup_event():
    await symbolic_pool.init_pool()
    start_metrics_server()

@metrics_app.on_event("shutdown")
async def shutdown_event():
    await symbolic_pool.close_pool()

@metrics_app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
