from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, StringConstraints, field_validator, model_validator

from api.utils.security_filter import security_filter


ALLOWED_SUBJECTS = {
    "Mathematics",
    "Science",
    "History",
    "Technology",
    "General",
}


class ExplainRequest(BaseModel):
    topic: Annotated[
        str, 
        StringConstraints(min_length=3, max_length=500, strip_whitespace=True)
    ]
    subject: Annotated[
        str, 
        StringConstraints(strip_whitespace=True)
    ] = "General"

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        # security_filter already strips HTML and normalizes whitespace
        return security_filter.filter_input(value)

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, value: str) -> str:
        if value not in ALLOWED_SUBJECTS:
            raise ValueError(f"Subject must be one of: {', '.join(ALLOWED_SUBJECTS)}")
        return value


class ExplanationOutput(BaseModel):
    definition: Annotated[str, StringConstraints(min_length=10, strip_whitespace=True)]
    mechanism: Annotated[str, StringConstraints(min_length=10, strip_whitespace=True)]
    example: Annotated[str, StringConstraints(min_length=10, strip_whitespace=True)]


class ExplainResponse(BaseModel):
    topic_id: UUID
    normalized_topic: str
    explanation: ExplanationOutput
    summary: str
    cached: bool
    response_ms: int

    @classmethod
    def placeholder(cls, topic: str) -> "ExplainResponse":
        return cls(
            topic_id=uuid4(),
            normalized_topic=topic.strip(),
            explanation=ExplanationOutput(
                definition="Placeholder definition pending AI integration.",
                mechanism="Placeholder mechanism pending AI integration.",
                example="Placeholder example pending AI integration.",
            ),
            summary="Placeholder summary pending AI integration.",
            cached=False,
            response_ms=0,
        )


class SummaryOutput(BaseModel):
    summary: Annotated[str, StringConstraints(min_length=30, strip_whitespace=True)]

    @model_validator(mode="after")
    def validate_word_count(self) -> "SummaryOutput":
        # Relaxed word count validation
        word_count = len(self.summary.split())
        if word_count < 20:
            raise ValueError("Summary is too short.")
        return self


class QuizRequest(BaseModel):
    topic_id: UUID
    count: int = Field(default=5, ge=1, le=10)
    difficulty: Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True)] = "medium"

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, value: str) -> str:
        if value not in {"easy", "medium", "hard"}:
            raise ValueError("Difficulty must be one of: easy, medium, hard.")
        return value


class QuizQuestion(BaseModel):
    id: int
    question: Annotated[str, StringConstraints(min_length=10, strip_whitespace=True)]
    options: list[Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]]
    correct_index: int = Field(ge=0, le=3)
    explanation: Annotated[str, StringConstraints(min_length=10, strip_whitespace=True)]

    @field_validator("options")
    @classmethod
    def validate_options(cls, value: list[str]) -> list[str]:
        if len(value) != 4:
            raise ValueError("Each quiz question must have exactly 4 options.")
        return value


class QuizGenerationOutput(BaseModel):
    questions: list[QuizQuestion]

    @model_validator(mode="after")
    def validate_question_list(self) -> "QuizGenerationOutput":
        if not 1 <= len(self.questions) <= 10:
            raise ValueError("Quiz must contain between 1 and 10 questions.")
        return self


class QuizResponse(BaseModel):
    quiz_id: UUID
    topic_id: UUID
    questions: list[QuizQuestion]

    @model_validator(mode="after")
    def validate_question_list(self) -> "QuizResponse":
        if not 1 <= len(self.questions) <= 10:
            raise ValueError("Quiz must contain between 1 and 10 questions.")
        return self

    @classmethod
    def placeholder(cls, topic_id: str) -> "QuizResponse":
        return cls(
            quiz_id=uuid4(),
            topic_id=UUID(topic_id),
            questions=[
                QuizQuestion(
                    id=1,
                    question="Placeholder quiz question?",
                    options=["Option A", "Option B", "Option C", "Option D"],
                    correct_index=0,
                    explanation="Placeholder explanation pending AI integration.",
                )
            ],
        )



class TopicResponse(BaseModel):
    topic_id: str
    normalized_topic: str
    subject: str | None = None

    @classmethod
    def from_explain_response(cls, payload: ExplainResponse) -> "TopicResponse":
        return cls(
            topic_id=str(payload.topic_id),
            normalized_topic=payload.normalized_topic,
            subject="General",
        )

    @classmethod
    def placeholder(cls, topic_id: str) -> "TopicResponse":
        return cls(
            topic_id=topic_id,
            normalized_topic="Placeholder Topic",
            subject="General",
        )
