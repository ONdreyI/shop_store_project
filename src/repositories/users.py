from pydantic import EmailStr
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UsersMapper
from src.models import UsersORM
from src.schemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UsersMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)
