from src.models.products_with_services import ProductsWithServicesServices
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import (
    ProductsWithServicesServicesSchemaMapper,
)


class ProductsWithServicesServicesRepository(BaseRepository):
    model = ProductsWithServicesServices
    mapper = ProductsWithServicesServicesSchemaMapper
