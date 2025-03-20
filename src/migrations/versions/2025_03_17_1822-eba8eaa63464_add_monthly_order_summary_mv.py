"""add_monthly_order_summary_mv

Revision ID: eba8eaa63464
Revises: e64b851e1ed8
Create Date: 2025-03-17 18:22:33.229103

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eba8eaa63464"
down_revision: Union[str, None] = "e64b851e1ed8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем материализованное представление
    op.execute(
        """
        CREATE MATERIALIZED VIEW monthly_order_summary AS
        SELECT 
            EXTRACT(YEAR FROM order_date)::integer as order_year,
            EXTRACT(MONTH FROM order_date)::integer as order_month,
            COUNT(id) as order_count,
            SUM(total_price) as total_order_value
        FROM orders
        GROUP BY 
            EXTRACT(YEAR FROM order_date),
            EXTRACT(MONTH FROM order_date);
    """
    )

    # Создаем индексы для оптимизации запросов
    op.execute(
        "CREATE UNIQUE INDEX ix_monthly_order_summary_pk ON monthly_order_summary (order_year, order_month)"
    )


def downgrade() -> None:
    # Удаляем представление и все связанные с ним объекты
    op.execute("DROP MATERIALIZED VIEW IF EXISTS monthly_order_summary CASCADE")
