# tests/conftest.py

import pytest
import asyncio
from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.api import app as main_app
from backend.async_engine import get_async_db
from backend.models import Base

# ─── Async Event Loop Fixture ───────────────────────────────────────
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

# ─── Override DB Dependency ─────────────────────────────────────────
@pytest.fixture(scope="function")
def override_get_db():
    async def _override():
        async for db in get_async_db():
            yield db
    return _override

# ─── FastAPI App Fixture ────────────────────────────────────────────
@pytest.fixture(scope="session")
def app():
    main_app.dependency_overrides[get_async_db] = override_get_db()
    return main_app

# ─── Test Client Fixture ────────────────────────────────────────────
@pytest.fixture(scope="session")
def client(app: FastAPI):
    return TestClient(app)

# ─── ESIL Fixture ───────────────────────────────────────────────────
@pytest.fixture
def esil_fixture():
    return {
        "dominant_emotion": "sadness",
        "emotion_id": "mock-id-123",
        "primary_emotion": "sadness",
        "intensity": 0.8,
        "confidence": 0.92,
        "timestamp_utc": "2025-04-30T12:00:00Z"
    }

# ─── Persona Fixture ────────────────────────────────────────────────
@pytest.fixture
def persona_fixture():
    return {
        "label": "soothing_ally",
        "tone": "calm",
        "goal": "comfort_user",
        "prompt": "Respond in a compassionate and steady tone."
    }

# ─── Atomese Code Fixture ───────────────────────────────────────────
@pytest.fixture
def mock_atomese_code():
    return "(EvaluationLink (PredicateNode \"Emotion\") (ListLink (ConceptNode \"X\") (ConceptNode \"Joy\")))"

# ─── Auth Middleware Stub ───────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def override_auth():
    import middleware.auth_required
    middleware.auth_required.auth_required = lambda fn: fn
    yield

# ─── Symbolic ZMQ Retry/Fallback Logic Test ─────────────────────────
def test_symbolic_pool_retry(monkeypatch, mock_atomese_code):
    from backend.services.symbolic_client_pool import symbolic_pool

    async def mock_send_fail(code):
        raise Exception("Simulated symbolic failure")

    monkeypatch.setattr(symbolic_pool, "send", mock_send_fail)

    with pytest.raises(Exception):
        asyncio.run(symbolic_pool.send(mock_atomese_code))
