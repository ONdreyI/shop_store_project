from sqlalchemy import ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ProductsWithServicesORM(Base):
    __tablename__ = "products_with_services"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), index=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL)
    product: Mapped["ProductsORM"] = relationship("ProductsORM")
    service: Mapped["ServicesORM"] = relationship("ServicesORM")
