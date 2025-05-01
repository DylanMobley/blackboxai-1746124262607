import asyncio
import pytest
from httpx import AsyncClient
from backend.api import app

@pytest.mark.asyncio
async def test_load_api_respond():
    async with AsyncClient(app=app, base_url="http://test") as client:
        tasks = []
        for i in range(50):  # Simulate 50 concurrent requests
            payload = {"text": f"Hello {i}"}
            headers = {"Authorization": "Bearer test-token"}
            tasks.append(client.post("/api/respond", json=payload, headers=headers))
        responses = await asyncio.gather(*tasks)
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
