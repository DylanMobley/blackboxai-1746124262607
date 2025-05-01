import pytest
from backend.services.memory_store import set_memory, get_memory

@pytest.mark.asyncio
async def test_memory_set_and_get():
    key = "test_key"
    value = {"emotion": "joy", "intensity": 0.9}

    set_memory(key, value)
    cached = get_memory(key)

    assert cached == value

@pytest.mark.asyncio
async def test_memory_get_nonexistent():
    assert get_memory("nonexistent_key") is None
