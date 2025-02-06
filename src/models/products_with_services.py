from sqlalchemy import ForeignKey, DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ProductsWithServicesORM(Base):
    __tablename__ = "products_with_services"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    service_ids: Mapped[str] = mapped_column(
        String, nullable=True
    )  # Хранение списка service_id в виде строки
    price: Mapped[DECIMAL] = mapped_column(DECIMAL)
    product: Mapped["ProductsORM"] = relationship("ProductsORM")
    services: Mapped[list["ServicesORM"]] = relationship(
        "ServicesORM", secondary="products_with_services_services"
    )


# Вспомогательная таблица для хранения связей многие-ко-многим
class ProductsWithServicesServices(Base):
    __tablename__ = "products_with_services_services"

    product_with_service_id: Mapped[int] = mapped_column(
        ForeignKey("products_with_services.id"), primary_key=True
    )
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), primary_key=True)
