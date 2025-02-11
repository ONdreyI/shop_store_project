from src.models import OrdersORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import OrdersMapper


class OrdersRepository(BaseRepository):
    model = OrdersORM
    mapper = OrdersMapper
