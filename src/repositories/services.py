from repositories.base import BaseRepository
from src.models.services import ServicesORM
from src.schemas.services import Services


class ServicesRepository(BaseRepository):
    model = ServicesORM
    schema = Services
