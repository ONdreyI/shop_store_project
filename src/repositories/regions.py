from src.models import RegionsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RegionsMapper


class RegionsRepository(BaseRepository):
    model = RegionsORM
    mapper = RegionsMapper
