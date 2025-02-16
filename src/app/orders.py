import logging
from datetime import date

from fastapi import APIRouter, HTTPException, Body, Query
from src.app.dependencies import DBDep, UserIdDep
from src.schemas.orders import Orders, OrdersAdd, OrdersAddRequest, OrderUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/orders",
    tags=["Заказы"],
)


@router.get("", name="Получение всех заказов")
async def get_orders(
    db: DBDep,
    start_date: date | None = Query(None, example="2023-01-01"),
    end_date: date | None = Query(None, example="2023-01-01"),
    page: int = 1,
    per_page: int = 10,
):
    if end_date < start_date:
        raise HTTPException(
            status_code=401,
            detail="Дата окончания должна быть больше даты начала",
        )
    try:
        return await db.orders.filter_by_time_with_pagination(
            start_date=start_date,
            end_date=end_date,
            page=page,
            per_page=per_page,
        )
    except Exception as e:
        logger.error(f"Error getting orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{order_id}", name="Получение заказа")
async def get_order(
    order_id: int,
    db: DBDep,
):
    """
    Получает заказ по его ID вместе со списком продуктов и сервисов.
    :param order_id: ID заказа для получения.
    :return: Заказ с продуктами и сервисами.
    """
    try:
        # Получаем заказ
        order_data = await db.orders.get_one_or_none_order(order_id)
        if order_data is None:
            logger.error(f"Заказ не найден, id: {order_id}")
            raise HTTPException(status_code=404, detail="Заказ не найден")

        return order_data

    except Exception as e:
        logger.error(f"Ошибка при получении заказа: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", name="Добавление заказа")
async def add_order(
    db: DBDep,
    user_id: UserIdDep,
    order_data: OrdersAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Новый заказ",
                "value": {
                    "order_date": "2023-10-10",
                    "customer_id": 15,
                    "manager_id": 1,
                    "region_id": 2,
                    "product_ids": [131, 132, 162],  # Список ID продуктов
                    "service_ids": [16, 17, 25],  # Список ID сервисов
                },
            }
        }
    ),
):
    # Преобразуем данные запроса в схему OrdersAdd
    _order_data = OrdersAdd(
        user_id=user_id,
        **order_data.dict(
            exclude={"product_ids", "service_ids"}
        ),  # Исключаем product_ids и service_ids
    )

    try:
        # Используем обновленный метод add для создания заказа
        await db.orders.add_order(
            data=_order_data,
            product_ids=order_data.product_ids,  # Передаем список ID продуктов
            service_ids=order_data.service_ids,  # Передаем список ID сервисов
        )
        return {"status": "OK"}
    except ValueError as e:
        # Обработка ошибок, связанных с отсутствием продуктов или сервисов
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Обработка других ошибок
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{order_id}", name="Редактирование заказа")
async def update_order(
    db: DBDep,
    order_id: int,
    order_data: OrderUpdate,
):
    """
    Обновляет заказ, добавляя или удаляя продукты и сервисы.
    :param order_id: ID заказа для редактирования.
    :param order_data: Данные для обновления заказа.
    :return: Обновленный заказ.
    """
    try:
        # Проверяем существование заказа
        order = await db.orders.get_one_ore_none(id=order_id)
        if order is None:
            logger.error(f"Заказ не найден, id: {order_id}")
            raise HTTPException(status_code=404, detail="Заказ не найден")

        # Обновляем заказ
        updated_order = await db.orders.edit_order(
            order_id=order_id,
            add_product_ids=order_data.add_product_ids,
            remove_product_ids=order_data.remove_product_ids,
            add_service_ids=order_data.add_service_ids,
            remove_service_ids=order_data.remove_service_ids,
        )

        return {"status": "OK", "data": updated_order}

    except Exception as e:
        logger.error(f"Ошибка при обновлении заказа: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{order_id}", name="Удаление заказа")
async def delete_order(
    order_id: int,
    db: DBDep,
):
    """
    Удаляет заказ по его ID.
    :param order_id: ID заказа для удаления.
    :return: Сообщение об успешном удалении.
    """
    try:
        # Проверяем существование заказа
        order = await db.orders.get_one_ore_none(id=order_id)
        if order is None:
            logger.error(f"Заказ не найден, id: {order_id}")
            raise HTTPException(status_code=404, detail="Заказ не найден")

        # Удаляем заказ
        await db.orders.delete_one(id=order_id)
        await db.commit()

        logger.info(f"Заказ удален, id: {order_id}")
        return {"status": "OK", "details": "Заказ удален"}

    except Exception as e:
        logger.error(f"Ошибка при удалении заказа: {e}")
        raise HTTPException(status_code=500, detail=str(e))
