from pydantic import BaseModel
from sqlalchemy import select, delete, insert, update

from src.database import async_session_maker
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None
    schema: BaseModel = None

    def __init__(self, session: async_session_maker):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        # return [self.schema.model_validate(model) for model in result.scalars().all()]
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_one_ore_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        # return self.schema.model_validate(model)
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        # return self.schema.model_validate(model)
        return self.mapper.map_to_domain_entity(model)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete_one(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
