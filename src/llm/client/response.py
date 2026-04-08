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
    core: List[str]
    context: List[str]
    work_model: List[str]
    compensation: List[str]
