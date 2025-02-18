from repositories.base import BaseRepository
from src.models import ManagersORM
from src.repositories.mappers.mappers import ManagersMapper


class ManagersRepository(BaseRepository):
    model = ManagersORM
    mapper = ManagersMapper
