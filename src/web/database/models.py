from sqlalchemy import (Column, String,
                        Integer, Boolean,
                        ForeignKey, Text,
                        BigInteger)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)


class Teams(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(25), nullable=False)
    owner_id = Column(BigInteger,
                      ForeignKey("users.id", ondelete="CASCADE"),
                      nullable=False)
    is_closed = Column(Boolean, default=False)
    code = Column(String(10), unique=True, default=None)


class Members(Base):
    __tablename__ = "members"

    user_id = Column(BigInteger,
                     ForeignKey("users.id", ondelete="CASCADE"),
                     primary_key=True)
    team_id = Column(Integer,
                     ForeignKey("teams.id", ondelete="CASCADE"),
                     primary_key=True)
    destiny = Column(BigInteger, default=None)


class Wishes(Base):
    __tablename__ = "wishes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    url = Column(Text, nullable=True)
    owner_id = Column(BigInteger,
                      ForeignKey("users.id", ondelete="CASCADE"),
                      nullable=False)
    is_selected = Column(Boolean, default=False)
