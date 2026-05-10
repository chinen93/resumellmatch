from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


@dataclass
class Skill:
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


@dataclass
class StarMetadata:
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
    id: Optional[int] = None
    user_id: Optional[int] = None
    raw_text: str = ""
    input_hash: Optional[str] = None
    full_text: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class User:
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    star_metadatas: List[StarMetadata] = field(default_factory=list)


@dataclass
class JobDescription:
    id: Optional[int] = None
    url: str = ""
    title: str = ""
    raw_text: str = ""
    created_at: Optional[datetime] = None


@dataclass
class JobDescriptionParsed:
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
    resume_id: Optional[int] = None
    job_description_parsed_id: Optional[int] = None
    score: int = 0
    llm_analysis: str = ""


@dataclass
class LLMCache:
    id: Optional[int] = None
    prompt_hash: str = ""
    prompt_text: str = ""
    response_hash: str = ""
    response_json: str = ""
    llm_name: Optional[str] = None
    created_at: Optional[datetime] = None
