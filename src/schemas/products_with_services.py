from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class ProductsWithServicesAdd(BaseModel):
    product_id: int = Field(..., description="ID продукта")
    service_ids: Optional[List[int]] = Field(None, description="Список ID услуг")
    price: Decimal = Field(None, max_digits=10, decimal_places=2)


class ProductsWithServices(ProductsWithServicesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductsWithServicesPatch(BaseModel):
    product_id: int | None = None
    service_id: int | None = None
    price: Decimal | None = Field(None, max_digits=10, decimal_places=2)


class ProductsWithServicesServices(BaseModel):
    services: List[int] = Field(..., description="Список ID услуг")
    price: Decimal = Field(..., max_digits=10, decimal_places=2)


class ProductsWithServicesServicesPatch(BaseModel):
    services: List[int] = Field(None, description="Список ID услуг")
    # price: Decimal = Field(None, max_digits=10, decimal_places=2)
