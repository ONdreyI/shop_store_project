import pytest
from datetime import date
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool
from src.schemas.orders import OrdersAdd, OrdersAddRequest


async def test_add_order():
    # Используем контекстный менеджер вместо фикстуры
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        # Сначала создадим пользователя, если его нет
        # Проверим, есть ли таблица users и создадим запись
        try:
            # Подготовим данные заказа
            order_data = OrdersAddRequest(
                order_date=date(2024, 2, 23),
                customer_id=1,  # Используем тестового клиента
                manager_id=1,   # Используем тестового менеджера
                region_id=1,    # Используем тестовый регион
                product_ids=[1, 2],  # Используем тестовые продукты
                service_ids=[1, 2]   # Используем тестовые сервисы
            )

            # Преобразуем в схему OrdersAdd
            # Используем user_id=None, чтобы обойти ограничение внешнего ключа
            _order_data = OrdersAdd(
                user_id=None,  # Установим None вместо 1
                **order_data.model_dump(exclude={"product_ids", "service_ids"})
            )

            # Добавляем заказ
            new_order = await db.orders.add_order(
                data=_order_data,
                product_ids=order_data.product_ids,
                service_ids=order_data.service_ids
            )

            # Проверяем, что заказ создан
            assert new_order is not None
            assert new_order.customer_id == order_data.customer_id
            assert new_order.manager_id == order_data.manager_id
            assert new_order.region_id == order_data.region_id
            
            # Проверяем продукты и сервисы заказа
            order_with_details = await db.orders.get_one_or_none_order(new_order.id)
            assert len(order_with_details.products) == 2
            assert len(order_with_details.services) == 2
            
        except Exception as e:
            # Выводим информацию об ошибке для отладки
            print(f"Test error: {e}")
            raise