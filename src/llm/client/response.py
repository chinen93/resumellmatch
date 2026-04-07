from typing import List

from pydantic import BaseModel


class SimpleResponse(BaseModel):
    text: List[str]


class ExtractKeywordResponse(BaseModel):
    candidate_name: str
    roles: List[str]
    technical_skills: List[str]
    soft_skills: List[str]
    responsabilities: List[str]
    ownership: List[str]
    achievements: List[str]
    methodologies: List[str]
