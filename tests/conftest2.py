import pytest
import json
from datetime import datetime
from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from sqlalchemy import text
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from app.dependencies import get_db  # noqa: E402
from src.config import settings  # noqa: E402
from src.database import (
    Base,
    engine_null_pool,
    async_session_maker_null_pool,
)  # noqa: E402
from src.models import *  # noqa
from src.logging_config import logger  # noqa: E402
from src.main import app  # noqa: E402
from utils.db_manager import DBManager  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
async def check_database():
    logger.info("ЗАПУСК ФИКСТУРЫ")
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool()


@pytest.fixture(scope="session", autouse=True)
async def set_database(check_database):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
        await conn.run_sync(Base.metadata.create_all)

        # Add default roles
        await conn.execute(
            RolesORM.__table__.insert(),
            [
                {"name": "user", "permissions": "basic_access"},
                {
                    "name": "manager",
                    "permissions": "order_management,customer_management",
                },
                {"name": "admin", "permissions": "full_access"},
            ],
        )
        logger.info("Созданы роли")

        # Load mock data from JSON files
        mock_data_path = Path("tests/mock_data")
        if mock_data_path.exists():
            try:
                # Load categories
                categories_file = mock_data_path / "categories.json"
                if categories_file.exists():
                    with open(categories_file, encoding="utf-8") as f:
                        categories_data = json.load(f)
                        await conn.execute(
                            CategoriesORM.__table__.insert(), categories_data
                        )
                        logger.info("Загружены тестовые категории")

                # Load customers
                customers_file = mock_data_path / "customers.json"
                if customers_file.exists():
                    with open(customers_file, encoding="utf-8") as f:
                        customers_data = json.load(f)
                        # Convert string dates to datetime.date objects
                        for customer in customers_data:
                            customer["birth_date"] = datetime.strptime(
                                customer["birth_date"], "%Y-%m-%d"
                            ).date()
                        await conn.execute(
                            CustomersORM.__table__.insert(), customers_data
                        )
                        logger.info("Загружены тестовые клиенты")

                # Load managers
                managers_file = mock_data_path / "managers.json"
                if managers_file.exists():
                    with open(managers_file, encoding="utf-8") as f:
                        managers_data = json.load(f)
                        await conn.execute(
                            ManagersORM.__table__.insert(), managers_data
                        )
                        logger.info("Загружены тестовые менеджеры")

                # Load regions
                regions_file = mock_data_path / "regions.json"
                if regions_file.exists():
                    with open(regions_file, encoding="utf-8") as f:
                        regions_data = json.load(f)
                        await conn.execute(RegionsORM.__table__.insert(), regions_data)
                        logger.info("Загружены тестовые регионы")

                # Load products
                products_file = mock_data_path / "products.json"
                if products_file.exists():
                    with open(products_file, encoding="utf-8") as f:
                        products_data = json.load(f)
                        await conn.execute(
                            ProductsORM.__table__.insert(), products_data
                        )
                        logger.info("Загружены тестовые продукты")

                # Load services
                services_file = mock_data_path / "services.json"
                if services_file.exists():
                    with open(services_file, encoding="utf-8") as f:
                        services_data = json.load(f)
                        await conn.execute(
                            ServicesORM.__table__.insert(), services_data
                        )
                        logger.info("Загружены тестовые сервисы")
            except Exception as e:
                logger.error(f"Error loading mock data: {e}")


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    # FastAPICache.init(InMemoryBackend(), prefix="test-cache")  # Инициализация кэша
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(set_database, ac):
    response = await ac.post(
        "/auth/register",
        json={
            "username": "nikname",
            "email": "kot@pes.com",
            "password": "123422222",
            "role_id": 1,
        },
    )
    logger.info(f"User registration response: {response.status_code}")
