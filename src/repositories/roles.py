from repositories.base import BaseRepository
from src.models import RolesORM
from src.schemas.roles import Role


class RolesRepository(BaseRepository):
    model = RolesORM
    schema = Role
