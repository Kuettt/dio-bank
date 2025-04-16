import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import db

class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(sa.String, nullable=True, unique=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped[list["Role"]] = relationship(back_populates="user")  # Use o nome da classe como string
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, username={self.username!r}, active={self.active!r})"
        )
