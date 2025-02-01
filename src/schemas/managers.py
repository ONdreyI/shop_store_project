from pydantic import BaseModel, Field


class ManagersAdd(BaseModel):
    first_name: str = Field(..., max_length=200)
    last_name: str = Field(..., max_length=200)
    department: str = Field(..., max_length=200)


class Managers(ManagersAdd):
    id: int


class ManagersPatch(BaseModel):
    first_name: str | None = Field(None, max_length=200)
    last_name: str | None = Field(None, max_length=200)
    department: str | None = Field(None, max_length=200)
