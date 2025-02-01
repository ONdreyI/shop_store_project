from pydantic import BaseModel, Field


class CategoriesAdd(BaseModel):
    name: str = Field(..., max_length=200)


class Categories(CategoriesAdd):
    id: int


class CategoriesPatch(BaseModel):
    name: str | None = Field(None, max_length=200)
