from sqlalchemy import String, Index, Date, func, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class CustomersORM(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), index=True)
    last_name: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    phone: Mapped[str] = mapped_column(String(20), index=True)
    address: Mapped[str] = mapped_column(Text, index=True)
    birth_date: Mapped[Date] = mapped_column(Date, index=True)

    __table_args__ = (
        Index("ix_customers_full_name", first_name, last_name),
        Index("ix_customers_contact_info", email, phone),
        Index("ix_customers_birth_year", func.extract("year", birth_date)),
        Index("ix_customers_address", address, postgresql_using="gin"),
    )
