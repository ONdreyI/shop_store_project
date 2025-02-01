from src.schemas.managers import Managers
from src.models import ManagersORM
from src.schemas.users import User
from src.models import UsersORM
from src.schemas.customers import Customers
from src.models import CustomersORM
from src.schemas.categories import Categories
from src.models import CategoriesORM
from src.schemas.services import Services
from src.models import ServicesORM
from src.repositories.mappers.base import DataMapper


class ServicesMapper(DataMapper):
    db_model = ServicesORM
    schema = Services


class CategoriesMapper(DataMapper):
    db_model = CategoriesORM
    schema = Categories


class CustomersMapper(DataMapper):
    db_model = CustomersORM
    schema = Customers


class UsersMapper(DataMapper):
    db_model = UsersORM
    schema = User


class ManagersMapper(DataMapper):
    db_model = ManagersORM
    schema = Managers
