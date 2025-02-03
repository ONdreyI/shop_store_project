from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class ProductsAdd(BaseModel):
    name: str = Field(..., max_length=200)
    category_id: int
    price: Decimal = Field(..., max_digits=10, decimal_places=2)


class Products(ProductsAdd):
    id: int


class ProductsPatch(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    category_id: Optional[int]
    price: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
