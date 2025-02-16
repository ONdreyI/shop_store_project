from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from decimal import Decimal


class OrdersAdd(BaseModel):
    order_date: date = Field(..., description="Дата заказа")
    customer_id: int = Field(..., description="ID клиента")
    manager_id: int = Field(..., description="ID менеджера")
    region_id: int = Field(..., description="ID региона")
    user_id: int = Field(..., description="ID пользователя")
    # product_ids: List[int] = Field(..., description="Список ID продуктов")
    # service_ids: List[int] = Field(..., description="Список ID сервисов")
    total_price: Optional[Decimal] = Field(
        default=None, description="Общая стоимость заказа"
    )


class Orders(OrdersAdd):
    id: int = Field(..., description="ID заказа")


class OrdersAddRequest(BaseModel):
    order_date: date = Field(..., description="Дата заказа")
    customer_id: int = Field(..., description="ID клиента")
    manager_id: int = Field(..., description="ID менеджера")
    region_id: int = Field(..., description="ID региона")
    product_ids: List[int] = Field(..., description="Список ID продуктов")
    service_ids: List[int] = Field(..., description="Список ID сервисов")
