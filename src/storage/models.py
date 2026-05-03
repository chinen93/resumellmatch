from datetime import date, datetime

from sqlalchemy import TIMESTAMP, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String, Text


class Base(DeclarativeBase):
    pass


class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    star_entries = relationship(
        "StarEntry",
        secondary="star_entries_skills_assoc",
        back_populates="skills",
    )

    def __repr__(self):
        return f"Skill(" f"id={self.id}, " f"name={self.name}, " ")"


class StarEntrySkillAssociation(Base):
    __tablename__ = "star_entries_skills_assoc"
    star_entry_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("star_entries.id"), primary_key=True
    )
    skill_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("skills.id"), primary_key=True
    )


class StarEntry(Base):
    __tablename__ = "star_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    metadata_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("star_metadatas.id"), primary_key=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    situation: Mapped[str] = mapped_column(String, nullable=False)
    task: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    result: Mapped[str] = mapped_column(String, nullable=False)
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

    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    type: Mapped[str] = mapped_column(
        String, nullable=False
    )  # education, project, work
    title: Mapped[str] = mapped_column(
        String, nullable=False
    )  # job title, degree, project name
    subtitle: Mapped[str] = mapped_column(
        String, nullable=False
    )  # company, school, etc.
    location: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(
        Date, nullable=True
    )  # if null, still working on it
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)

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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    raw_text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)

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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    raw_text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)

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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_description_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("job_descriptions.id"), primary_key=True
    )
    input_hash: Mapped[str] = mapped_column(String, nullable=True, index=True)
    full_response: Mapped[str] = mapped_column(Text, nullable=True)
    summary: Mapped[str] = mapped_column(String, nullable=False)
    required_skills: Mapped[str] = mapped_column(
        String, nullable=False
    )  # CSV separated skills from JD
    prefered_skills: Mapped[str] = mapped_column(
        String, nullable=False
    )  # CSV separated skills from JD
    keywords: Mapped[str] = mapped_column(
        String, nullable=False
    )  # CSV separated keywords from JD

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

    resume_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("resumes.id"), primary_key=True
    )
    job_description_parsed_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("job_descriptions_parsed.id"), primary_key=True
    )

    score: Mapped[int] = mapped_column(Integer, nullable=False)
    llm_analysis: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return (
            f"Match("
            f"resume_id={self.resume_id}, "
            f"job_description_parsed_id={self.job_description_parsed_id}), "
            f"score={self.score}"
            # f"llm_analysis={self.llm_analysis}"
            f")"
        )


class LLMCache(Base):
    __tablename__ = "llm_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    prompt_hash: Mapped[str] = mapped_column(String, nullable=False, index=True)
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    response_hash: Mapped[str] = mapped_column(String, nullable=False, index=True)
    response_json: Mapped[str] = mapped_column(Text, nullable=False)
    llm_name: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)

    def __repr__(self):
        return f"LLMCache(id={self.id}, prompt_hash={self.prompt_hash}, response_hash={self.response_hash})"
