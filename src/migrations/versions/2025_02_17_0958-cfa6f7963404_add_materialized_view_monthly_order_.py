"""Add materialized view monthly_order_summary

Revision ID: cfa6f7963404
Revises: f3596e9cc9c2
Create Date: 2025-02-17 09:58:01.880535

"""

from typing import Sequence, Union
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cfa6f7963404"
down_revision: Union[str, None] = "f3596e9cc9c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
    CREATE MATERIALIZED VIEW monthly_order_summary AS
    SELECT 
        EXTRACT(YEAR FROM order_date) AS order_year,
        EXTRACT(MONTH FROM order_date) AS order_month,
        COUNT(id) AS order_count,
        SUM(total_price) AS total_order_value
    FROM orders
    GROUP BY order_year, order_month;
    """
    )


def downgrade() -> None:
    op.execute("DROP MATERIALIZED VIEW IF EXISTS monthly_order_summary;")
