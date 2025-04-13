from src.schemas.categories import CategoriesAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool
from src.logging_config import logger


async def test_add_category(db: DBManager):
    data = CategoriesAdd(name="Кухоннаяа мебель")
    await db.categories.add(data)
    logger.info(f"{data}")
    await db.commit()
