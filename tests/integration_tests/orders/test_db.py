import json
from decimal import Decimal

import pytest
from datetime import date

from logging_config import logger
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool
from src.schemas.orders import OrdersAdd, OrdersAddRequest


async def test_add_order():
    # Используем контекстный менеджер вместо фикстуры
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        # Сначала создадим пользователя, если его нет
        # Проверим, есть ли таблица users и создадим запись
        try:
            # Подготовим данные заказа
            order_data = OrdersAddRequest(
                order_date=date(2024, 2, 23),
                customer_id=(await db_.customers.get_all())[
                    0
                ].id,  # Используем тестового клиента
                manager_id=(await db_.managers.get_all())[
                    0
                ].id,  # Используем тестового менеджера
                region_id=(await db_.regions.get_all())[
                    0
                ].id,  # Используем тестовый регион
                product_ids=[
                    (await db_.products.get_all())[0].id,
                    (await db_.products.get_all())[1].id,
                ],  # Используем тестовые продукты
                service_ids=[
                    (await db_.services.get_all())[0].id,
                    (await db_.services.get_all())[1].id,
                ],  # Используем тестовые сервисы
            )

            # Преобразуем в схему OrdersAdd
            # Используем user_id=None, чтобы обойти ограничение внешнего ключа
            _order_data = OrdersAdd(
                user_id=1,
                **order_data.model_dump(exclude={"product_ids", "service_ids"}),
            )

            # Добавляем заказ
            new_order = await db_.orders.add_order(
                data=_order_data,
                product_ids=order_data.product_ids,
                service_ids=order_data.service_ids,
            )

            # Проверяем, что заказ создан
            assert new_order is not None
            assert new_order.customer_id == order_data.customer_id
            assert new_order.manager_id == order_data.manager_id
            assert new_order.region_id == order_data.region_id

            # Проверка поля total в заказах
            with open(
                "tests\\mock_data\\services.json", "r", encoding="utf-8)"
            ) as file:
                data = json.load(file)
                services_prices = data[0]["price"] + data[1]["price"]
            with open(
                "tests\\mock_data\\products.json", "r", encoding="utf-8)"
            ) as file:
                data = json.load(file)
                products_prices = data[0]["price"] + data[1]["price"]
            total_order_price = (await db_.orders.get_all())[0].total_price
            assert total_order_price == services_prices + products_prices
            logger.info("ПРОВЕРКА СУММ ДЛЯ ПОЛЯ TOTAL_PRICE")
            # assert len(order_with_details.products) == 2
            # assert len(order_with_details.services) == 2

            # Проверка получения заказа

        except Exception as e:
            # Выводим информацию об ошибке для отладки
            print(f"Test error: {e}")
            raise
