import pytest
from sqlalchemy import text

from src.config import settings
from src.database import Base, engine_null_pool
from src.models import *  # noqa
from src.logging_config import logger


@pytest.fixture(scope="session", autouse=True)
async def async_main():
    logger.info("Я ФИКСТУРА")
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
        await conn.run_sync(Base.metadata.create_all)
