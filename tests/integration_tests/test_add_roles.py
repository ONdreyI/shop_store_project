# async def test_add_role():
#     role_data = RoleAdd(name="user", permissions="basic_access")
#     async with DBManager(session_factory=async_session_maker) as db:
#         await db.roles.add(role_data)
#         logger.info("Роль создана успешно!")
#         await db.commit()
