from sqlalchemy import ForeignKey, DECIMAL, Date, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class OrdersORM(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_date: Mapped[Date] = mapped_column(Date, index=True, nullable=False)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), index=True, nullable=False
    )
    manager_id: Mapped[int] = mapped_column(
        ForeignKey("managers.id"), index=True, nullable=False
    )
    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id"), index=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )
    product_with_services_id: Mapped[int] = mapped_column(
        ForeignKey("products_with_services.id"), index=True, nullable=False
    )

    customer: Mapped["CustomersORM"] = relationship("CustomersORM")
    manager: Mapped["ManagersORM"] = relationship("ManagersORM")
    region: Mapped["RegionsORM"] = relationship("RegionsORM")
    user: Mapped["UsersORM"] = relationship("UsersORM")
    product_with_services: Mapped["ProductsWithServicesORM"] = relationship(
        "ProductsWithServicesORM", back_populates="order"
    )

    __table_args__ = (
        Index("ix_orders_order_date", order_date),
        Index("ix_orders_customer_id", customer_id),
        Index("ix_orders_manager_id", manager_id),
        Index("ix_orders_region_id", region_id),
        Index("ix_orders_user_id", user_id),
        Index("ix_orders_product_service_id", product_with_services_id),
    )
