from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Teams(Base):
    __tablename__ = "teams"

    title: Mapped[str]
    owner: Mapped[str]
    is_closed: Mapped[bool] = mapped_column(default=False)


# class Members(Base):
#     __tablename__ = "members"

#     user_id: Mapped[str]
#     worker_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))


# class Wishes(Base):
#     __tablename__ = "wishes"

#     title: Mapped[str]
#     url: Mapped[Optional[str]]
#     owner: Mapped[str]
#     is_selected: Mapped[bool] = mapped_column(default=False)
