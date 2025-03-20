from src.schemas.roles import RoleAdd
from src.utils.db_manager import DBManager
from src.database import async_session_maker
from src.logging_config import logger


# async def test_add_role():
#     role_data = RoleAdd(name="user", permissions="basic_access")
#     async with DBManager(session_factory=async_session_maker) as db:
#         await db.roles.add(role_data)
#         logger.info("Роль создана успешно!")
#         await db.commit()
