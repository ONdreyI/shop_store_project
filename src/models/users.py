from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), index=True)
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    role: Mapped["RolesORM"] = relationship("RolesORM")

    __table_args__ = (
        Index("ix_users_username", username, unique=True),
        Index("ix_users_email", email, unique=True),
        Index("ix_users_role_id", role_id),
    )
