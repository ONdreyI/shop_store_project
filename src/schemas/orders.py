from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal


class OrdersAdd(BaseModel):
    order_date: date = Field(..., description="Дата заказа")
    customer_id: int = Field(..., description="ID клиента")
    manager_id: int = Field(..., description="ID менеджера")
    region_id: int = Field(..., description="ID региона")
    user_id: int = Field(..., description="ID пользователя")
    product_with_services_id: int = Field(..., description="ID продукта с услугами")


class Orders(OrdersAdd):
    id: int = Field(..., description="ID заказа")
