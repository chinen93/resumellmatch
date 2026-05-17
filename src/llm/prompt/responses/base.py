from abc import ABC
from typing import List

from pydantic import BaseModel


class BaseResponse(BaseModel, ABC):
    pass


class SimpleResponse(BaseResponse):
    text: List[str]
