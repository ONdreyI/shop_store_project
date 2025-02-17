from pydantic import BaseModel, Field
from decimal import Decimal


class MonthlyOrderSummaryRead(BaseModel):
    """
    Pydantic схема для данных из материализованного представления MonthlyOrderSummaryORM.
    """

    order_year: int = Field(..., description="Год заказа")
    order_month: int = Field(..., description="Месяц заказа")
    order_count: int = Field(..., description="Количество заказов")
    total_order_value: Decimal = Field(..., description="Общая стоимость заказов")
