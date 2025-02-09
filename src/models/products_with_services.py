from sqlalchemy import ForeignKey, DECIMAL, Integer, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class ProductsWithServicesORM(Base):
    __tablename__ = "products_with_services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    service_ids: Mapped[list[int]] = mapped_column(
        ARRAY(Integer), nullable=True
    )  # Используем массив
    price: Mapped[DECIMAL] = mapped_column(DECIMAL)

    product: Mapped["ProductsORM"] = relationship("ProductsORM")
    services: Mapped[list["ServicesORM"]] = relationship(
        "ServicesORM",
        secondary="products_with_services_services",
        cascade="all",
    )


# Вспомогательная таблица для хранения связей многие-ко-многим
class ProductsWithServicesServices(Base):
    __tablename__ = "products_with_services_services"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )  # Добавлен первичный ключ
    product_with_service_id: Mapped[int] = mapped_column(
        ForeignKey("products_with_services.id", ondelete="CASCADE"), index=True
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="CASCADE"), index=True
    )
