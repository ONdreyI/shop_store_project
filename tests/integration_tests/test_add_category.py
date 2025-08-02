from src.schemas.categories import CategoriesAdd
from src.logging_config import logger


async def test_add_category(db):
    data = CategoriesAdd(name="Кухоннаяа мебель второй категории")
    await db.categories.add(data)
    logger.info(f"{data}")
    await db.commit()
