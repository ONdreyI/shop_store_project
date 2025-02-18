from sqlalchemy import text
from src.models import MonthlyOrderSummaryORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.views import MonthlyOrderSummaryMapper
from src.logging_config import logger  # Импортируем логгер


class MonthlyOrderSummaryRepository(BaseRepository):
    model = MonthlyOrderSummaryORM
    mapper = MonthlyOrderSummaryMapper

    async def refresh_monthly_order_summary(self):
        """
        Обновляет материализованное представление monthly_order_summary.
        """
        query = text("REFRESH MATERIALIZED VIEW monthly_order_summary;")
        logger.info("Refreshing materialized view: monthly_order_summary")

        await self.session.execute(query)
        await self.session.commit()  # Фиксируем изменения, если это необходимо
        logger.info("Materialized view refreshed successfully")

        # Получаем обновленные данные из представления
        select_query = text("SELECT * FROM monthly_order_summary;")
        logger.debug(f"Executing query to fetch data: {select_query}")

        result = await self.session.execute(select_query)
        rows = result.fetchall()
        logger.debug(f"Fetched {len(rows)} rows from monthly_order_summary")

        return [self.mapper.map_to_domain_entity(model) for model in rows]
