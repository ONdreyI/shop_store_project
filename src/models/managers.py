from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ManagersORM(Base):
    __tablename__ = 'managers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(200), index=True)
    last_name: Mapped[str] = mapped_column(String(200), index=True)
    department: Mapped[str] = mapped_column(String(200), index=True)
