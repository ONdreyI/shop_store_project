from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class ProductsWithServicesAdd(BaseModel):
    product_id: int = Field(..., description="ID продукта")
    service_ids: Optional[List[int]] = Field(None, description="Список ID услуг")
    price: Decimal = Field(None, max_digits=10, decimal_places=2)


class ProductsWithServices(ProductsWithServicesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductsWithServicesPatch(BaseModel):
    product_id: Optional[int] = Field(None, description="ID продукта")
    service_ids: Optional[List[int]] = Field(None, description="Список ID услуг")


class ProductsWithServicesServices(BaseModel):
    product_with_service_id: int = Field(..., description="ID продукта с сервисом")
    service_id: int = Field(..., description="ID услуги")
