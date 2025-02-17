from sqlalchemy import text

from src.models import MonthlyOrderSummaryORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.views import MonthlyOrderSummaryMapper


class MonthlyOrderSummaryRepository(BaseRepository):
    model = MonthlyOrderSummaryORM
    mapper = MonthlyOrderSummaryMapper

    async def refresh_monthly_order_summary(self):
        """
        Обновляет материализованное представление monthly_order_summary.
        """
        query = text("REFRESH MATERIALIZED VIEW monthly_order_summary;")
        await self.session.execute(query)
        await self.session.commit()  # Фиксируем изменения, если это необходимо

        # Получаем обновленные данные из представления
        select_query = text("SELECT * FROM monthly_order_summary;")
        result = await self.session.execute(select_query)
        return [self.mapper.map_to_domain_entity(model) for model in result.fetchall()]
