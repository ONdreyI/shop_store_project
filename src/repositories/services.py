from src.models.services import ServicesORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ServicesMapper


class ServicesRepository(BaseRepository):
    model = ServicesORM
    mapper = ServicesMapper
