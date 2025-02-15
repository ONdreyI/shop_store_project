from src.schemas.orders import Orders
from src.models import OrdersORM
from src.models import CategoriesORM
from src.models import CustomersORM
from src.models import ManagersORM
from src.models import ProductsORM
from src.models import ProductsWithServicesORM
from src.models import RegionsORM
from src.models import ServicesORM
from src.models import UsersORM
from src.repositories.mappers.base import DataMapper
from src.schemas.categories import Categories
from src.schemas.customers import Customers
from src.schemas.managers import Managers
from src.schemas.products import Products, ProductWithCategoryResponse
from src.schemas.products_with_services import (
    ProductsWithServices,
    ProductsWithServicesServices,
)
from src.schemas.regions import Regions
from src.schemas.services import Services
from src.schemas.users import User


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


class RegionsMapper(DataMapper):
    db_model = RegionsORM
    schema = Regions


class ProductsMapper(DataMapper):
    db_model = ProductsORM
    schema = Products


class ProductWithCategoryMapper(DataMapper):
    db_model = ProductsORM
    schema = ProductWithCategoryResponse


class ProductsWithServicesMapper(DataMapper):
    db_model = ProductsWithServicesORM
    schema = ProductsWithServices


class OrdersMapper(DataMapper):
    db_model = OrdersORM
    schema = Orders
