import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.asyncio
async def test_get_managers():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/managers")
        print(f"Response: {response.text}")
        assert response.status_code == 200, f"Failed with response: {response.text}"
        data = response.json()
        assert isinstance(data, list), "Expected a list of managers"
