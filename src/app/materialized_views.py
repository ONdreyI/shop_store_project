import logging

from fastapi import APIRouter

from src.schemas.views.monthly_order_summary import MonthlyOrderSummaryRead
from src.app.dependencies import DBDep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/materialized_views",
    tags=["Анализ данных"],
)


@router.post("/refresh-monthly-order-summary", description="Анализ заказов по месяцам")
async def refresh_monthly_order_summary_route(db: DBDep):
    data = await db.monthly_order_summary.refresh_monthly_order_summary()
    return {"status": "OK", "data": [data]}
