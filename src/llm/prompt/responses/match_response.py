from src.llm.prompt.responses.base import BaseResponse


class MatchJobWithStarResponse(BaseResponse):
    score: int
    explanation: str
