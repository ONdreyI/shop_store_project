from src.schemas.categories import CategoriesAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker
from src.logging_config import logger


async def test_add_category():
    data = CategoriesAdd(name="Кухоннаяа мебель")
    async with DBManager(session_factory=async_session_maker) as db:
        await db.categories.add(data)
        logger.info(f"{data}")
        await db.commit()
