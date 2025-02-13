import logging
from datetime import date

from fastapi import APIRouter, HTTPException, Body, Query
from src.app.dependencies import DBDep, UserIdDep
from src.schemas.orders import Orders, OrdersAdd, OrdersAddRequest

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
                    "product_with_services_id": 23,
                },
            }
        }
    ),
):
    _order_data = OrdersAdd(
        user_id=user_id,
        **order_data.dict(),
    )

    try:
        await db.orders.add(_order_data)
        await db.commit()
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
