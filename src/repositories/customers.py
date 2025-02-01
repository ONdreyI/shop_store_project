from src.models import CustomersORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import CustomersMapper


class CustomersRepository(BaseRepository):
    model = CustomersORM
    mapper = CustomersMapper
