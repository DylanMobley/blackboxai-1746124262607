import asyncio
import pytest
from modules.emotion_memory import EmotionMemory

@pytest.mark.asyncio
async def test_emotion_memory_store_and_retrieve():
    memory = EmotionMemory(redis_url="redis://localhost:6379")
    await memory.connect()

    user_id = 123
    emotion_state = {
        "primary_emotion": "happy",
        "intensity": 0.8,
        "confidence": 0.9
    }

    await memory.store_emotion_state(user_id, emotion_state)
    trajectory = await memory.get_emotion_trajectory(user_id, limit=10)

    assert len(trajectory) > 0
    assert any(entry["emotion_state"]["primary_emotion"] == "happy" for entry in trajectory)

    await memory.close()
