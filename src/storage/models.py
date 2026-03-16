from datetime import datetime

from sqlalchemy import TIMESTAMP, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String


class Base(DeclarativeBase):
    pass


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)
    star_entries = relationship(
        "StarEntry",
        secondary="star_entries_skills_assoc",
        back_populates="skills",
    )

    def __repr__(self):
        return f"Skill(" f"id={self.id}, " f"name={self.name}, " ")"


class StarEntrySkillAssociation(Base):
    __tablename__ = "star_entries_skills_assoc"
    star_entry_id = Column(Integer, ForeignKey("star_entries.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)


class StarEntry(Base):
    __tablename__ = "star_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    metadata_id = Column(Integer, ForeignKey("star_metadatas.id"))
    title = Column(String, nullable=False)
    situation = Column(String, nullable=False)
    task = Column(String, nullable=False)
    action = Column(String, nullable=False)
    result = Column(String, nullable=False)
    # skills = relationship(
    #    StarEntrySkillAssociation, cascade="all, delete-orphan", lazy=False
    # )
    skills = relationship(
        "Skill",
        secondary="star_entries_skills_assoc",
        back_populates="star_entries",
        cascade="all",
        lazy=False,
    )

    updated_at = Column(TIMESTAMP, default=datetime.now)
    created_at = Column(TIMESTAMP, default=datetime.now)

    def __repr__(self):
        return (
            f"StarEntry("
            f"id={self.id}, "
            f"metadata_id={self.metadata_id}, "
            f"title={self.title}, "
            f"situation={self.situation}, "
            f"task={self.task}, "
            f"action={self.action}, "
            f"result={self.result}, "
            f"skills={self.skills}"
            ")"
        )


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

    entries = relationship(
        StarEntry, backref="star_entries.id", cascade="all, delete-orphan", lazy=False
    )

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
