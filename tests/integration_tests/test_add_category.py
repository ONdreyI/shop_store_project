from src.schemas.categories import CategoriesAdd
<<<<<<< HEAD
from src.logging_config import logger


async def test_add_category(db):
    data = CategoriesAdd(name="Кухоннаяа мебель второй категории")
=======
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool
from src.logging_config import logger


async def test_add_category(db: DBManager):
    data = CategoriesAdd(name="Кухоннаяа мебель")
>>>>>>> 42d8a6137fd0e22eef098d5eabd90c6a81366444
    await db.categories.add(data)
    logger.info(f"{data}")
    await db.commit()
