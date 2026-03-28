from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class TopicModel(Base):
    __tablename__ = "topics"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    session_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("sessions.id"))
    raw_input: Mapped[str] = mapped_column(Text)
    normalized_topic: Mapped[str] = mapped_column(Text)
    subject: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    llm_model: Mapped[str] = mapped_column(String(100))
    cached: Mapped[bool] = mapped_column(Boolean, default=False)
