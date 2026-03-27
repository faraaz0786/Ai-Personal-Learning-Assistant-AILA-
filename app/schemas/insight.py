from pydantic import BaseModel


class QuizInsightSchema(BaseModel):
    strengths: str
    weaknesses: str
    what_to_improve: str
    recommendation: str


class MentorTipSchema(BaseModel):
    tip: str
    focus_area: str
    recommendation: str
