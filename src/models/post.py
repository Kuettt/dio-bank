import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import db
from datetime import datetime

class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(
        sa.DateTime, default=lambda: datetime.now()
    )
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    author: Mapped[str] = mapped_column(sa.ForeignKey("user.username"))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, title={self.title}, author={self.author}, author_id={self.author_id})"
