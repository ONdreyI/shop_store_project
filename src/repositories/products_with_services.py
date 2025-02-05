from repositories.base import BaseRepository
from src.models import ProductsWithServicesORM
from src.schemas.products_with_services import ProductsWithServices


class ProductsWithServicesRepository(BaseRepository):
    model = ProductsWithServicesORM
    mapper = ProductsWithServices
