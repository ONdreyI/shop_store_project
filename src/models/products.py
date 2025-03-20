from sqlalchemy import String, ForeignKey, DECIMAL, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ProductsORM(Base):
    __tablename__ = "products"
    # __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    price: Mapped[DECIMAL] = mapped_column(DECIMAL)

    category: Mapped["CategoriesORM"] = relationship("CategoriesORM")
    orders: Mapped[list["OrdersORM"]] = relationship(
        "OrdersORM", secondary="order_products", back_populates="products"
    )

    __table_args__ = (
        Index("ix_products_name", name),
        Index("ix_products_category_id", category_id),
        Index("ix_products_price", price),
    )
