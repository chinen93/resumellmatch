from abc import ABC
from typing import List

from pydantic import BaseModel


class BaseResponse(BaseModel, ABC):
    pass


class SimpleResponse(BaseResponse):
    text: List[str]


class ExtractKeywordResponse(BaseResponse):
    candidate_name: str
    roles: List[str]
    technical_skills: List[str]
    soft_skills: List[str]
    responsabilities: List[str]
    ownership: List[str]
    achievements: List[str]
    methodologies: List[str]


class JobDescriptionResponse(BaseResponse):
    job_description: str


class JobDescriptioKeywordsResponse(BaseResponse):
    summary: str
    role: List[str]
    technical_skills: List[str]
    soft_skills: List[str]
    responsabilities: List[str]
    ownership: List[str]
    tools: List[str]
    methodologies: List[str]
    domain_knowledge: List[str]
    work_model: List[str]
    compensation: List[str]


class MatchJobWithStarResponse(BaseResponse):
    score: int
    explanation: str


class RewriteStarResponse(BaseResponse):
    bullet_point: str
