from sqlalchemy import DateTime, ForeignKey, Integer, String, func, JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class QuizModel(Base):
    __tablename__ = "quizzes"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    topic_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("topics.id"))
    questions: Mapped[list[dict]] = mapped_column(JSON)
    question_count: Mapped[int] = mapped_column(Integer, default=5)
    difficulty: Mapped[str] = mapped_column(String(20), default="medium")
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
