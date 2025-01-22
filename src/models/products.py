from sqlalchemy import String, ForeignKey, DECIMAL, Index, func
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ProductsORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL, index=True)
    category: Mapped["CategoriesORM"] = relationship("CategoriesORM")
    tsv: Mapped[TSVECTOR] = mapped_column(TSVECTOR)

    __table_args__ = (Index("ix_products_tsv", tsv, postgresql_using="gin"),)

    @staticmethod
    def __set_tsvector():
        return func.to_tsvector("english", ProductsORM.name)
