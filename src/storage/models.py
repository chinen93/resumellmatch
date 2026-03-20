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


class Resume(Base):

    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    raw_text = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)

    def __repr__(self):
        return (
            f"Resume("
            f"id={self.id}, "
            f"user_id={self.user_id}), "
            f"created_at={self.created_at}"
            f")"
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
        return (
            f"User("
            f"id={self.id}, "
            f"name={self.name}, "
            f"email={self.email}, "
            f"star_metadatas={self.star_metadatas}"
            f")"
        )


class JobDescription(Base):

    __tablename__ = "job_descriptions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    raw_text = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)

    def __repr__(self):
        return (
            f"JobDescription("
            f"id={self.id}, "
            f"url={self.url}, "
            f"title={self.title}"
            f")"
        )


class JobDescriptionParsed(Base):

    __tablename__ = "job_descriptions_parsed"
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"))
    summary = Column(String, nullable=False)
    required_skills = Column(String, nullable=False)  # CSV separated skills from JD
    prefered_skills = Column(String, nullable=False)  # CSV separated skills from JD
    keywords = Column(String, nullable=False)  # CSV separated keywords from JD

    def __repr__(self):
        return (
            f"JobDescriptionParsed("
            f"id={self.id}, "
            f"job_description_id={self.job_description_id}), "
            f"summary={self.summary}"
            f")"
        )


class Matches(Base):

    __tablename__ = "matches"

    resume_id = Column(Integer, ForeignKey("resumes.id"), primary_key=True)
    job_description_parsed_id = Column(
        Integer, ForeignKey("job_descriptions_parsed.id"), primary_key=True
    )

    score = Column(Integer, nullable=False)
    llm_analysis = Column(String, nullable=False)

    def __repr__(self):
        return (
            f"Match("
            f"resume_id={self.resume_id}, "
            f"job_description_parsed_id={self.job_description_parsed_id}), "
            f"score={self.score}"
            # f"llm_analysis={self.llm_analysis}"
            f")"
        )
