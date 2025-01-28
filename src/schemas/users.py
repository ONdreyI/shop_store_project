from typing import ClassVar, Optional

from pydantic import BaseModel, ConfigDict, constr, Field, EmailStr, conint
from pydantic.v1 import validator


class UserRequestAdd(BaseModel):
    username: str = Field(..., max_length=200)
    email: EmailStr
    password: constr(min_length=8) = Field(
        ...,
        description="Пароль должен быть не менее 8 символов и содержать хотя бы одну цифру, одну заглавную и одну строчную букву",
    )
    role_id: conint(ge=1, le=4) = Field(
        ..., description="Идентификатор роли пользователя (от 1 до 4)"
    )


class UserAdd(BaseModel):
    username: str = Field(..., max_length=200)
    email: EmailStr
    hashed_password: str
    role_id: int = Field(..., description="Идентификатор роли пользователя")


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    role_id: int

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
