from sqlalchemy import String, ForeignKey, DECIMAL, Index, func, event
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ProductsORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL, index=True)
    category: Mapped["CategoriesORM"] = relationship("CategoriesORM")

    __table_args__ = (
        Index("ix_products_name", name),
        Index("ix_products_category_id", category_id),
        Index("ix_products_price", price),
    )
