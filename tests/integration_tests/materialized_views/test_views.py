import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_refresh_monthly_order_summary(ac: AsyncClient):
    # Make request to refresh materialized view
    response = await ac.get("/materialized_views/refresh-monthly-order-summary")
    
    # Check response status code
    assert response.status_code == 200
    
    # Check response structure
    data = response.json()
    assert "status" in data
    assert "data" in data
    assert data["status"] == "OK"
    assert isinstance(data["data"], list)
    
    # Check data content
    summary_data = data["data"][0]
    assert isinstance(summary_data, dict)
    
    # Check required fields in summary
    expected_fields = ["month", "year", "total_orders", "total_amount"]
    for field in expected_fields:
        assert field in summary_data, f"Missing field: {field}"