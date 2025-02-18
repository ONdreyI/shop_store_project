from datetime import date
from pydantic import BaseModel
from sqlalchemy import select, delete, insert, update, and_
from src.database import async_session_maker
from src.repositories.mappers.base import DataMapper
from src.logging_config import logger  # Импортируем логгер


class BaseRepository:
    model = None
    mapper: DataMapper = None
    schema: BaseModel = None

    def __init__(self, session: async_session_maker):
        self.session = session

    async def apply_pagination(self, query, page: int = 1, per_page: int = 10):
        """
        Попробовать реализовать единую пагинацию для всех методов и моделей.
        Пока не использую нигде
        :param query:
        :param page:
        :param per_page:
        :return:
        """
        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)
        logger.debug(f"Applying pagination: page={page}, per_page={per_page}")

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all(self):
        query = select(self.model)
        logger.debug(f"Executing get_all query: {query}")

        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def filter_by_time_with_pagination(
        self,
        start_date: date = None,
        end_date: date = None,
        page: int = 1,
        per_page: int = 10,
    ):
        query = select(self.model)

        if start_date and end_date:
            query = query.where(
                and_(
                    self.model.order_date >= start_date,
                    self.model.order_date <= end_date,
                )
            )
            logger.debug(
                f"Filtering by time: start_date={start_date}, end_date={end_date}"
            )

        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)
        logger.debug(f"Applying pagination: page={page}, per_page={per_page}")

        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_all_with_pagination(
        self,
        page: int,
        per_page: int,
    ):
        query = select(self.model)
        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)
        logger.debug(
            f"Executing get_all_with_pagination query: page={page}, per_page={per_page}"
        )

        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_one_ore_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        logger.debug(f"Executing get_one_ore_none query: {query}")

        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            logger.warning(f"No record found with filter: {filter_by}")
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        logger.info(f"Adding new record: {data}")

        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        logger.info(f"Updating record with filter: {filter_by}")

        await self.session.execute(update_stmt)
        await self.session.commit()

    async def delete_one(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        logger.warning(f"Deleting record with filter: {filter_by}")

        await self.session.execute(delete_stmt)
