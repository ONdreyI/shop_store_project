from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class RolesORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), index=True)
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    role: Mapped["RolesORM"] = relationship("RolesORM")
