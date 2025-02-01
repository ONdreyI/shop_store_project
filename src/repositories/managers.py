from src.repositories.mappers.mappers import ManagersMapper
from src.models import ManagersORM
from repositories.base import BaseRepository
from src.models import RolesORM
from src.schemas.roles import Role


class ManagersRepository(BaseRepository):
    model = ManagersORM
    mapper = ManagersMapper
