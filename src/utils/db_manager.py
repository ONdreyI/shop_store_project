from src.repositories.managers import ManagersRepository
from src.repositories.customers import CustomersRepository
from src.repositories.categories import CategoriesRepository
from src.repositories.roles import RolesRepository
from src.repositories.services import ServicesRepository
from src.repositories.users import UsersRepository


class DBManager:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.services = ServicesRepository(self.session)
        self.users = UsersRepository(self.session)
        self.roles = RolesRepository(self.session)
        self.categories = CategoriesRepository(self.session)
        self.customers = CustomersRepository(self.session)
        self.managers = ManagersRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
