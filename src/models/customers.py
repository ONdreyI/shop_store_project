from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class CustomersORM(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(200), index=True)
    last_name: Mapped[str] = mapped_column(String(200), index=True)
    contact_info: Mapped[str] = mapped_column(String(200), index=True)
