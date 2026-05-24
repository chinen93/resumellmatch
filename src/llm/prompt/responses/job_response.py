from src.llm.prompt.responses.base import BaseResponse


class JobDescriptionResponse(BaseResponse):
    job_description: str


class JobDescriptioKeywordsResponse(BaseResponse):
    summary: str
    role: str
    technical_skills: str
    soft_skills: str
    responsabilities: str
    ownership: str
    tools: str
    methodologies: str
    domain_knowledge: str
    work_model: str
    compensation: str


class JobSummaryResponse(BaseResponse):
    summary: str


class JobRoleResponse(BaseResponse):
    role: str


class JobTechSkillResponse(BaseResponse):
    skills: str


class JobSoftSkillResponse(BaseResponse):
    skills: str


class JobResponsabilitiesResponse(BaseResponse):
    responsabilities: str


class JobToolsResponse(BaseResponse):
    tools: str


class JobWorkModelResponse(BaseResponse):
    work_model: str


class JobCompensationResponse(BaseResponse):
    compensation: str


class JobOwnershipResponse(BaseResponse):
    ownership: str


class JobDomainKnowledgeResponse(BaseResponse):
    domain: str


class JobMethodologiesResponse(BaseResponse):
    summary: str
