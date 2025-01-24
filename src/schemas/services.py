from pydantic import BaseModel, Field, condecimal


class ServicesAdd(BaseModel):
    name: str = Field(..., max_length=200)
    price: condecimal(max_digits=10, decimal_places=2)


class Services(ServicesAdd):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class ServicesPatch(BaseModel):
    name: str | None = Field(None, max_length=200)
    price: condecimal(max_digits=10, decimal_places=2) | None = None
