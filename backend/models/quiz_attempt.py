from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class QuizAttemptModel(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    quiz_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    session_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"))
    answers: Mapped[list[int]] = mapped_column(JSONB)
    score: Mapped[int] = mapped_column(Integer)
    max_score: Mapped[int] = mapped_column(Integer)
    percentage: Mapped[float] = mapped_column(Numeric(5, 2))
    time_taken_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    attempted_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
