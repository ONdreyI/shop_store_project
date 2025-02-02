from pydantic import BaseModel, Field


class RegionsAdd(BaseModel):
    name: str = Field(..., max_length=200)


class Regions(RegionsAdd):
    id: int


class RegionsPatch(BaseModel):
    name: str | None = Field(None, max_length=200)
