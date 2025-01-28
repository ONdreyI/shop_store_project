from pydantic import BaseModel, Field, condecimal, ConfigDict


from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class RoleAdd(BaseModel):
    name: str = Field(..., max_length=200)
    permissions: str = Field(..., max_length=200)


class Role(RoleAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RolePatch(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    permissions: Optional[str] = Field(None, max_length=200)
