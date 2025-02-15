from sqlalchemy import String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ServicesORM(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL, index=True)

    orders: Mapped[list["OrdersORM"]] = relationship(
        "OrdersORM", secondary="order_services", back_populates="services"
    )
