import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import db
from .base import db

class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    user: Mapped[list["User"]] = relationship(back_populates="role")  # Use o nome da classe como string

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.username!r})"