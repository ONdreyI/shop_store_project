from sqlalchemy import String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ServicesORM(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL, index=True)
