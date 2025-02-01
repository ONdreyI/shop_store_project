from src.schemas.services import Services
from src.models import ServicesORM
from src.repositories.mappers.base import DataMapper


class ServicesMapper(DataMapper):
    db_model = ServicesORM
    schema = Services
