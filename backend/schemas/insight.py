from typing import Union, List
from pydantic import BaseModel, field_validator


class QuizInsightSchema(BaseModel):
    strengths: Union[str, List[str]]
    weaknesses: Union[str, List[str]]
    what_to_improve: Union[str, List[str]]
    recommendation: Union[str, List[str]]

    @field_validator("strengths", "weaknesses", "what_to_improve", "recommendation", mode="before")
    @classmethod
    def ensure_string(cls, v):
        if isinstance(v, list):
            return " ".join(v)
        return str(v)


class MentorTipSchema(BaseModel):
    tip: Union[str, List[str]]
    focus_area: Union[str, List[str]]
    recommendation: Union[str, List[str]]

    @field_validator("tip", "focus_area", "recommendation", mode="before")
    @classmethod
    def ensure_string(cls, v):
        if isinstance(v, list):
            return " ".join(v)
        return str(v)
