from src.models import CategoriesORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import CategoriesMapper


class CategoriesRepository(BaseRepository):
    model = CategoriesORM
    mapper = CategoriesMapper
