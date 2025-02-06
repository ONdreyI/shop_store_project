from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ProductsWithServicesAdd(BaseModel):
    product_id: int = Field(..., description="ID продукта")
    service_id: Optional[int] = Field(None, description="ID услуги (опционально)")
    price: Decimal = Field(None, max_digits=10, decimal_places=2)


class ProductsWithServices(ProductsWithServicesAdd):
    id: int


class ProductsWithServicesPatch(BaseModel):
    product_id: int | None = None
    service_id: int | None = None
    price: Decimal | None = Field(None, max_digits=10, decimal_places=2)
