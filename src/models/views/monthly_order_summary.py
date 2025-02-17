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


monthly_order_summary = materialized_view(
    "monthly_order_summary",
    select(
        func.extract("year", OrdersORM.order_date).label("order_year"),
        func.extract("month", OrdersORM.order_date).label("order_month"),
        func.count(OrdersORM.id).label("order_count"),
        func.sum(OrdersORM.total_price).label("total_order_value"),
    ).group_by(
        "order_year", "order_month"
    ),  # Оставляем один раз
)
