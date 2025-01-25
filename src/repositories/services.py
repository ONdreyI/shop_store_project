from src.models.services import ServicesORM
from repositories.base import BaseRepository


class ServicesRepository(BaseRepository):
    model = ServicesORM


print(dir(ServicesRepository))
