# ruff: noqa: E402
import json
from typing import AsyncGenerator
from unittest import mock

from schemas.categories import CategoriesAdd
from schemas.customers import CustomersAdd
from schemas.managers import ManagersAdd
from schemas.products import ProductsAdd
from schemas.regions import RegionsAdd
from schemas.roles import RoleAdd
from schemas.services import ServicesAdd

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest

from src.app.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *  # noqa
from httpx import AsyncClient, ASGITransport

from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_data/categories.json", encoding="utf-8") as file_categories:
        categories = json.load(file_categories)
    with open("tests/mock_data/customers.json", encoding="utf-8") as file_customers:
        customers = json.load(file_customers)
    with open("tests/mock_data/managers.json", encoding="utf-8") as file_managers:
        managers = json.load(file_managers)
    with open("tests/mock_data/regions.json", encoding="utf-8") as file_regions:
        regions = json.load(file_regions)
    with open("tests/mock_data/products.json", encoding="utf-8") as file_products:
        products = json.load(file_products)
    with open("tests/mock_data/services.json", encoding="utf-8") as file_services:
        services = json.load(file_services)
    with open("tests/mock_data/roles.json", encoding="utf-8") as file_roles:
        roles = json.load(file_roles)

    categories = [CategoriesAdd.model_validate(category) for category in categories]
    customers = [CustomersAdd.model_validate(customer) for customer in customers]
    managers = [ManagersAdd.model_validate(manager) for manager in managers]
    regions = [RegionsAdd.model_validate(region) for region in regions]
    products = [ProductsAdd.model_validate(product) for product in products]
    services = [ServicesAdd.model_validate(service) for service in services]
    roles = [RoleAdd.model_validate(role) for role in roles]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.categories.add_bulk(categories)
        await db_.customers.add_bulk(customers)
        await db_.managers.add_bulk(managers)
        await db_.regions.add_bulk(regions)
        await db_.products.add_bulk(products)
        await db_.services.add_bulk(services)
        await db_.roles.add_bulk(roles)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac: AsyncClient, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "username": "nikname",
            "email": "kot@pes.com",
            "password": "123422222",
            "role_id": 3,
        },
    )


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac: AsyncClient):
    await ac.post(
        "/auth/login",
        json={
            "username": "nikname",
            "email": "kot@pes.com",
            "password": "123422222",
            "role_id": 3,
        },
    )
    assert ac.cookies["access_token"]
    yield ac
