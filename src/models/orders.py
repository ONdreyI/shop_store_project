from sqlalchemy import ForeignKey, DECIMAL, Date, Index, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class OrdersORM(Base):
    __tablename__ = "orders"

    # Вспомогательная таблица для связи многие-ко-многим между ProductsORM и OrdersORM
    order_products = Table(
        "order_products",
        Base.metadata,
        Column("order_id", ForeignKey("orders.id"), primary_key=True),
        Column("product_id", ForeignKey("products.id"), primary_key=True),
    )

    # Вспомогательная таблица для связи многие-ко-многим между ServicesORM и OrdersORM
    order_services = Table(
        "order_services",
        Base.metadata,
        Column("order_id", ForeignKey("orders.id"), primary_key=True),
        Column("service_id", ForeignKey("services.id"), primary_key=True),
    )

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
    total_price: Mapped[DECIMAL] = mapped_column(DECIMAL, index=True, nullable=False)

    customer: Mapped["CustomersORM"] = relationship("CustomersORM")
    manager: Mapped["ManagersORM"] = relationship("ManagersORM")
    region: Mapped["RegionsORM"] = relationship("RegionsORM")
    user: Mapped["UsersORM"] = relationship("UsersORM")
    products: Mapped[list["ProductsORM"]] = relationship(
        "ProductsORM", secondary=order_products, back_populates="orders"
    )
    services: Mapped[list["ServicesORM"]] = relationship(
        "ServicesORM", secondary=order_services, back_populates="orders"
    )

    __table_args__ = (
        Index("ix_orders_order_date", order_date),
        Index("ix_orders_customer_id", customer_id),
        Index("ix_orders_manager_id", manager_id),
        Index("ix_orders_region_id", region_id),
        Index("ix_orders_user_id", user_id),
        Index("ix_orders_total_price", total_price),
    )
