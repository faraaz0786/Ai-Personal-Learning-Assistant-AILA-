from pydantic import BaseModel, field_validator


class ProgressSummary(BaseModel):
    topics_studied: int = 0
    average_score: float = 0.0
    streak_days: int = 0
    progress_percent: float = 0.0


class ProgressHistoryItem(BaseModel):
    topic: str
    score: float
    attempted_at: str


class PerformanceTrendItem(BaseModel):
    date: str
    score: float


class TopTopicItem(BaseModel):
    topic: str
    score: float


class DashboardSummary(BaseModel):
    total_topics: int = 0
    total_questions: int = 0
    accuracy: float = 0.0
    avg_score: float = 0.0
    streak: int = 0
    recent_activity: list[ProgressHistoryItem] = []
    performance_trend: list[PerformanceTrendItem] = []
    top_topics: list[TopTopicItem] = []


class ProgressRecommendation(BaseModel):
    topic: str
    reason: str
    type: str

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str) -> str:
        if value not in {"prerequisite", "related", "advanced"}:
            raise ValueError("Recommendation type must be prerequisite, related, or advanced.")
        return value
