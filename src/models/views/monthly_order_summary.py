from decimal import Decimal
import sqlalchemy as sa
from sqlalchemy import select, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.orders import OrdersORM
from src.database import Base
from src.utils.materialized_views import materialized_view


class MonthlyOrderSummaryORM(Base):
    """
    Материализованное представление для суммарных заказов по месяцам.
    """

    __tablename__ = "monthly_order_summary"

    order_year: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    order_month: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    order_count: Mapped[int] = mapped_column(sa.Integer)
    total_order_value: Mapped[Decimal] = mapped_column(sa.DECIMAL)


# Создание материализованного представления с использованием чистого SQL
# для обеспечения правильного определения первичного ключа.
monthly_order_summary = sa.DDL(
    """
    CREATE MATERIALIZED VIEW IF NOT EXISTS monthly_order_summary AS
    SELECT 
        EXTRACT(YEAR FROM order_date)::integer as order_year,
        EXTRACT(MONTH FROM order_date)::integer as order_month,
        COUNT(id) as order_count,
        SUM(total_price) as total_order_value
    FROM orders
    GROUP BY 
        EXTRACT(YEAR FROM order_date),
        EXTRACT(MONTH FROM order_date)
    WITH DATA;
"""
)

sa.event.listen(
    Base.metadata,
    "after_create",
    monthly_order_summary.execute_if(dialect="postgresql"),
)
