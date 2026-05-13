"""Domain models for the resume-LLM match application.

This module defines all core dataclasses that represent the main domain entities
in the resume-job-STAR matching system. These models are used throughout the
application for data representation, LLM processing, and storage operations.

Classes:
    Skill: Represents a technical or professional skill.
    StarEntry: Represents a single STAR (Situation, Task, Action, Result) story.
    StarMetadata: Container for STAR stories from a work/education/project experience.
    Resume: Represents a resume document.
    User: Represents a user entity with associated STAR stories.
    JobDescription: Represents a job posting.
    JobDescriptionParsed: Parsed job description with extracted keywords and skills.
    Match: Represents a resume-to-job match result with score.
    LLMCache: Cache entry for LLM responses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


@dataclass
class Skill:
    """Represents a professional or technical skill.

    Attributes:
        id: Unique identifier in the database.
        name: The skill name.
        created_at: Timestamp when the skill was created.
    """

    id: Optional[int] = None
    name: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class StarEntry:
    id: Optional[int] = None
    metadata_id: Optional[int] = None
    title: str = ""
    situation: str = ""
    task: str = ""
    action: str = ""
    result: str = ""
    skills: List[Skill] = field(default_factory=list)
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    def __repr__(self):
        """Return a formatted string representation of the STAR entry."""
        return (
            f"{self.title}: "
            f"{self.situation}. "
            f"{self.task}. "
            f"{self.action}. "
            f"{self.result}."
        )


@dataclass
class StarMetadata:
    """Represents metadata for a collection of STAR stories from a single experience.

    StarMetadata groups multiple STAR entries that come from the same work
    experience, education, or project, with contextual information about that
    experience.

    Attributes:
        id: Unique identifier in the database.
        user_id: Foreign key referencing the User who owns this experience.
        type: Type of experience (e.g., 'work', 'education', 'project').
        title: Title of the position/program/project.
        subtitle: Additional context (e.g., company name, school name).
        location: Geographic location of the experience.
        start_date: When the experience started.
        end_date: When the experience ended (None if ongoing).
        created_at: Timestamp when the metadata was created.
        entries: List of STAR entries from this experience.
    """

    id: Optional[int] = None
    user_id: Optional[int] = None
    type: str = ""
    title: str = ""
    subtitle: str = ""
    location: str = ""
    start_date: date = field(default_factory=date.today)
    end_date: Optional[date] = None
    created_at: Optional[datetime] = None
    entries: List[StarEntry] = field(default_factory=list)


@dataclass
class Resume:
    """Represents a resume document.

    Attributes:
        id: Unique identifier in the database.
        user_id: Foreign key referencing the User who owns this resume.
        raw_text: The original unprocessed text content of the resume.
        input_hash: SHA256 hash of the raw_text for deduplication and caching.
        full_text: The processed/enriched text after LLM enhancement.
        created_at: Timestamp when the resume was created.
    """

    id: Optional[int] = None
    user_id: Optional[int] = None
    raw_text: str = ""
    input_hash: Optional[str] = None
    full_text: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class User:
    """Represents a user of the resume-matching system.

    Attributes:
        id: Unique identifier in the database.
        name: The user's full name.
        email: The user's email address.
        star_metadatas: List of STAR experience records associated with this user.
    """

    id: Optional[int] = None
    name: str = ""
    email: str = ""
    star_metadatas: List[StarMetadata] = field(default_factory=list)


@dataclass
class JobDescription:
    """Represents a job posting or job description.

    Attributes:
        id: Unique identifier in the database.
        url: URL where the job was posted.
        title: Job title or position name.
        raw_text: The full text of the job description.
        created_at: Timestamp when the job was added to the system.
    """

    id: Optional[int] = None
    url: str = ""
    title: str = ""
    raw_text: str = ""
    created_at: Optional[datetime] = None


@dataclass
class JobDescriptionParsed:
    """Represents a parsed/processed job description with extracted information.

    Contains the results of LLM processing of a job description, including
    extracted keywords, required skills, and preferred qualifications.

    Attributes:
        id: Unique identifier in the database.
        job_description_id: Foreign key referencing the original JobDescription.
        input_hash: SHA256 hash of the job description for caching.
        full_response: The complete LLM response (raw output).
        summary: Brief summary of the job.
        required_skills: Skills that are required for the position.
        prefered_skills: Skills that are preferred but not required.
        keywords: Key terms extracted from the job description.
    """

    id: Optional[int] = None
    job_description_id: Optional[int] = None
    input_hash: Optional[str] = None
    full_response: Optional[str] = None
    summary: str = ""
    required_skills: str = ""
    prefered_skills: str = ""
    keywords: str = ""


@dataclass
class Match:
    """Represents a match between a resume and a job description.

    Contains the match result including the calculated score and LLM analysis
    of how well the resume aligns with the job requirements.

    Attributes:
        resume_id: Foreign key referencing the Resume being matched.
        job_description_parsed_id: Foreign key referencing the JobDescriptionParsed being matched against.
        score: Numeric score indicating match quality (0-100).
        llm_analysis: Detailed LLM analysis explaining the match or mismatch.
    """

    resume_id: Optional[int] = None
    job_description_parsed_id: Optional[int] = None
    score: int = 0
    llm_analysis: str = ""


@dataclass
class LLMCache:
    """Represents a cached LLM response for performance optimization.

    Caches LLM responses based on prompt hashes to avoid re-processing identical
    prompts, improving performance and reducing API/compute usage.

    Attributes:
        id: Unique identifier in the database.
        prompt_hash: SHA256 hash of the prompt used as cache key.
        prompt_text: The full text of the prompt.
        response_hash: SHA256 hash of the response.
        response_json: The LLM response in JSON format.
        llm_name: Name/identifier of the LLM model used.
        created_at: Timestamp when the cache entry was created.
    """

    id: Optional[int] = None
    prompt_hash: str = ""
    prompt_text: str = ""
    response_hash: str = ""
    response_json: str = ""
    llm_name: Optional[str] = None
    created_at: Optional[datetime] = None
