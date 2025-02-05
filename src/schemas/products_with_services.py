from decimal import Decimal

from pydantic import BaseModel, Field


class ProductsWithServicesAdd(BaseModel):
    product_id: int
    service_id: int
    price: Decimal = Field(..., max_digits=10, decimal_places=2)


class ProductsWithServices(ProductsWithServicesAdd):
    id: int


class ProductsWithServicesPatch(BaseModel):
    product_id: int | None = None
    service_id: int | None = None
    price: Decimal | None = Field(None, max_digits=10, decimal_places=2)
