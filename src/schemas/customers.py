from pydantic import BaseModel, Field, constr, EmailStr
from datetime import date
import re

# Регулярное выражение для валидации номера телефона в формате +7 911 8888888
phone_pattern = re.compile(r"^\+\d{1,3} \d{3} \d{7}$")


class CustomersAdd(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=255)
    phone: str = Field(
        ...,
        pattern=phone_pattern,
        max_length=20,
        description="Phone number with country and region prefix",
        example="+7 911 8888888",
    )
    address: str
    birth_date: date


class Customers(CustomersAdd):
    id: int


class CustomersPatch(BaseModel):
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    email: EmailStr | None = Field(None, max_length=255)
    phone: str | None = Field(
        None,
        pattern=phone_pattern,
        max_length=20,
        description="Phone number with country and region prefix",
        example="+7 911 888 88 88",
    )
    address: str | None = None
    birth_date: date | None = None
