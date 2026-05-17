from typing import List

from src.llm.prompt.responses.base import BaseResponse


class ExtractKeywordResponse(BaseResponse):
    candidate_name: str
    roles: List[str]
    technical_skills: List[str]
    soft_skills: List[str]
    responsabilities: List[str]
    ownership: List[str]
    achievements: List[str]
    methodologies: List[str]
