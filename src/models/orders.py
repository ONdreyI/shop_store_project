from sqlalchemy import ForeignKey, DECIMAL, Date, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class OrdersORM(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_date: Mapped[Date] = mapped_column(Date, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.id"), index=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), index=True)
    total_price: Mapped[DECIMAL] = mapped_column(DECIMAL, index=True)
    product: Mapped["ProductsORM"] = relationship("ProductsORM")
    customer: Mapped["CustomersORM"] = relationship("CustomersORM")
    manager: Mapped["ManagersORM"] = relationship("ManagersORM")
    region: Mapped["RegionsORM"] = relationship("RegionsORM")

    __table_args__ = (
        Index("ix_orders_order_date", order_date),
        Index("ix_orders_product_id", product_id),
        Index("ix_orders_customer_id", customer_id),
        Index("ix_orders_manager_id", manager_id),
        Index("ix_orders_region_id", region_id),
        Index("ix_orders_total_price", total_price),
    )
