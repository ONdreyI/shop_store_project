from sqlalchemy import insert

from src.schemas.services import Services
from src.models.services import ServicesORM
from repositories.base import BaseRepository


class ServicesRepository(BaseRepository):
    model = ServicesORM
    schema = Services
