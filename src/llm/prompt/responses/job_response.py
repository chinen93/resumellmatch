from typing import List

from src.llm.prompt.responses.base import BaseResponse


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


class JobSummaryResponse(BaseResponse):
    summary: str


class JobRoleResponse(BaseResponse):
    role: List[str]


class JobTechSkillResponse(BaseResponse):
    skills: List[str]


class JobSoftSkillResponse(BaseResponse):
    skills: List[str]


class JobResponsabilitiesResponse(BaseResponse):
    responsabilities: List[str]


class JobToolsResponse(BaseResponse):
    tools: List[str]


class JobWorkModelResponse(BaseResponse):
    work_model: List[str]


class JobCompensationResponse(BaseResponse):
    compensation: List[str]
