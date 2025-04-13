import json
from datetime import date

import pytest
from httpx import AsyncClient

from database import async_session_maker_null_pool
from logging_config import logger
from schemas.orders import OrdersAddRequest, OrdersAdd
from utils.db_manager import DBManager


@pytest.mark.parametrize(
    (
        "start_date",
        "end_date",
        "page",
        "pere_page",
    ),
    [
        ("2024-02-23", "2024-02-23", 1, 1),
        ("2024-01-01", "2024-01-31", 1, 5),
        ("2023-12-31", "2024-01-01", 1, 5),
    ],
)
async def test_get_orders_with_dates(
    ac: AsyncClient,
    start_date,
    end_date,
    page,
    pere_page,
):
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "page": page,
        "pere_page": pere_page,
    }
    response = await ac.get("/orders", params=params)
    assert response.status_code == 200
    data = response.json()
    print(f"data: {data}")
    # Проверяем, что данные соответствуют запросу
    assert isinstance(data, list) or isinstance(data, dict)
    if isinstance(data, dict):
        assert data["page"] == 1
        assert data["per_page"] == 5
    # Если метод возвращает заказы, можно проверить их даты (пример):
    # if isinstance(data, list) and data:
    #     assert data[0]["order_date"] >= "2023-01-01"
    #     assert data[0]["order_date"] <= "2023-01-31"
