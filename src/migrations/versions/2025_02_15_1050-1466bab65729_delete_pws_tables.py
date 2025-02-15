"""Delete pws tables

Revision ID: 1466bab65729
Revises: 3e91f319daf6
Create Date: 2025-02-15 10:50:08.655959

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1466bab65729"
down_revision: Union[str, None] = "3e91f319daf6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаление внешнего ключа
    op.drop_constraint(
        "orders_product_with_services_id_fkey", "orders", type_="foreignkey"
    )

    # Удаление индексов и таблиц с использованием CASCADE
    op.execute("DROP TABLE IF EXISTS products_with_services_services CASCADE")
    op.execute("DROP TABLE IF EXISTS products_with_services CASCADE")

    # Создание новых таблиц и индексов
    op.create_table(
        "order_products",
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.PrimaryKeyConstraint("order_id", "product_id"),
    )
    op.create_table(
        "order_services",
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
        ),
        sa.PrimaryKeyConstraint("order_id", "service_id"),
    )
    op.add_column("orders", sa.Column("total_price", sa.DECIMAL(), nullable=False))
    op.create_index(
        op.f("ix_orders_total_price"), "orders", ["total_price"], unique=False
    )
    op.drop_column("orders", "product_with_services_id")


def downgrade() -> None:
    # Восстановление внешнего ключа
    op.add_column(
        "orders",
        sa.Column(
            "product_with_services_id",
            sa.INTEGER(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.create_foreign_key(
        "orders_product_with_services_id_fkey",
        "orders",
        "products_with_services",
        ["product_with_services_id"],
        ["id"],
    )

    # Восстановление индексов и таблиц
    op.drop_index(op.f("ix_orders_total_price"), table_name="orders")
    op.create_index(
        "ix_orders_product_with_services_id",
        "orders",
        ["product_with_services_id"],
        unique=False,
    )
    op.create_index(
        "ix_orders_product_service_id",
        "orders",
        ["product_with_services_id"],
        unique=False,
    )
    op.drop_column("orders", "total_price")
    op.create_table(
        "products_with_services",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text(
                "nextval('products_with_services_id_seq'::regclass)"
            ),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("product_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("price", sa.NUMERIC(), autoincrement=False, nullable=False),
        sa.Column(
            "service_ids",
            postgresql.ARRAY(sa.INTEGER()),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name="products_with_services_product_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="products_with_services_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index(
        "ix_products_with_services_product_id",
        "products_with_services",
        ["product_id"],
        unique=False,
    )
    op.create_table(
        "products_with_services_services",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "product_with_service_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("service_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["product_with_service_id"],
            ["products_with_services.id"],
            name="products_with_services_services_product_with_service_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
            name="products_with_services_services_service_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="products_with_services_services_pkey"),
    )
    op.create_index(
        "ix_products_with_services_services_service_id",
        "products_with_services_services",
        ["service_id"],
        unique=False,
    )
    op.create_index(
        "ix_products_with_services_services_product_with_service_id",
        "products_with_services_services",
        ["product_with_service_id"],
        unique=False,
    )
    op.drop_table("order_services")
    op.drop_table("order_products")
