from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, StringConstraints, field_validator, model_validator

from app.schemas.learn import QuizQuestion
from app.schemas.progress import DashboardSummary
from app.schemas.insight import QuizInsightSchema


class QuizDetailResponse(BaseModel):
    quiz_id: UUID
    topic_id: UUID
    questions: list[QuizQuestion]

    @classmethod
    def placeholder(cls, quiz_id: UUID) -> "QuizDetailResponse":
        return cls(
            quiz_id=quiz_id,
            topic_id=uuid4(),
            questions=[
                QuizQuestion(
                    id=1,
                    question="Placeholder quiz question for the selected topic?",
                    options=["Option A", "Option B", "Option C", "Option D"],
                    correct_index=0,
                    explanation="Placeholder explanation for the correct answer.",
                )
            ],
        )


class QuizAttemptRequest(BaseModel):
    answers: list[Annotated[int, Field(ge=0, le=3)]] = Field(min_length=1)


class QuizAttemptResult(BaseModel):
    question_id: int
    correct: bool
    your_answer: int
    correct_index: int


class QuizAttemptResponse(BaseModel):
    attempt_id: UUID
    score: int
    max_score: int
    percentage: float
    results: list[QuizAttemptResult]
    analytics: DashboardSummary | None = None
    insights: QuizInsightSchema | None = None

    @model_validator(mode="after")
    def validate_result_shape(self) -> "QuizAttemptResponse":
        if self.max_score < 1:
            raise ValueError("max_score must be at least 1.")
        if self.score < 0 or self.score > self.max_score:
            raise ValueError("score must be between 0 and max_score.")
        return self

    @classmethod
    def placeholder(
        cls, quiz_id: UUID, answers: list[int]
    ) -> "QuizAttemptResponse":
        _ = quiz_id
        return cls(
            attempt_id=uuid4(),
            score=0,
            max_score=len(answers),
            percentage=0.0,
            results=[
                QuizAttemptResult(
                    question_id=index + 1,
                    correct=False,
                    your_answer=answer,
                    correct_index=0,
                )
                for index, answer in enumerate(answers)
            ],
        )
