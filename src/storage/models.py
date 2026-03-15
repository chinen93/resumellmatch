from datetime import datetime

from sqlalchemy import TIMESTAMP, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String


class Base(DeclarativeBase):
    pass


class StarMetadata(Base):

    __tablename__ = "star_metadatas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String, nullable=False)  # education, project, work
    title = Column(String, nullable=False)  # job title, degree, project name
    subtitle = Column(String, nullable=False)  # company, school, etc.
    location = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # if null, still working on it
    created_at = Column(TIMESTAMP, default=datetime.now)

    def __repr__(self):
        return (
            f"StarMetadata("
            f"id={self.id}, "
            f"user={self.user_id}, "
            f"title={self.title}, "
            f"subtitle={self.subtitle}"
            ")"
        )


class User(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    star_metadatas = relationship(
        StarMetadata, backref="users.id", cascade="all, delete-orphan", lazy=False
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email}, star_metadatas={self.star_metadatas})"
