from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class RolesORM(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)
    permissions: Mapped[str] = mapped_column(String(200))
