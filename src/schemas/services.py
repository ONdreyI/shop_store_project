from pydantic import BaseModel, Field, condecimal


class ServicesAdd(BaseModel):
    name: str = Field(..., max_length=200)
    price: condecimal(max_digits=10, decimal_places=2)


class Services(ServicesAdd):
    id: int
