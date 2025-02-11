import logging

from fastapi import APIRouter, HTTPException
from src.app.dependencies import DBDep
from src.schemas.orders import Orders, OrdersAdd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/orders",
    tags=["Заказы"],
)


@router.get("", name="Получение всех заказов")
async def get_orders(
    db: DBDep,
    page: int = 1,
    per_page: int = 10,
):
    try:
        return await db.orders.get_all_with_pagination(
            page=page,
            per_page=per_page,
        )
    except Exception as e:
        logger.error(f"Error getting orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))
