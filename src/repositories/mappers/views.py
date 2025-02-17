from src.schemas.views.monthly_order_summary import MonthlyOrderSummaryRead
from src.models import MonthlyOrderSummaryORM
from src.repositories.mappers.base import DataMapper


class MonthlyOrderSummaryMapper(DataMapper):
    db_model = MonthlyOrderSummaryORM
    schema = MonthlyOrderSummaryRead
