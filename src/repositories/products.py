from repositories.base import BaseRepository
from src.models import ProductsORM
from src.repositories.mappers.mappers import ProductsMapper


class ProductsRepository(BaseRepository):
    model = ProductsORM
    mapper = ProductsMapper
