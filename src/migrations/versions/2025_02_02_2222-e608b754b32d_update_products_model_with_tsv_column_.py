"""Update products model with tsv column russia

Revision ID: e608b754b32d
Revises: 71607565d8ce
Create Date: 2025-02-02 22:22:42.856600

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "e608b754b32d"
down_revision: Union[str, None] = "71607565d8ce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем столбец tsv
    op.drop_column("products", "tsv")
    # Добавляем столбец tsv и индекс для таблицы products
    op.add_column("products", sa.Column("tsv", postgresql.TSVECTOR(), nullable=False))
    op.create_index("ix_products_tsv", "products", ["tsv"], postgresql_using="gin")
    # Обновляем значение tsv для существующих записей (если необходимо)
    op.execute("UPDATE products SET tsv = to_tsvector('russian', name)")


def downgrade() -> None:
    # Удаляем индекс и столбец tsv из таблицы products при откате миграции
    op.drop_index("ix_products_tsv", table_name="products")
    op.drop_column("products", "tsv")
