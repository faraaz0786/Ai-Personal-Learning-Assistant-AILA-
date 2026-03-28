from sqlalchemy import DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class ExplanationModel(Base):
    __tablename__ = "explanations"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    topic_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id"), unique=True
    )
    definition: Mapped[str] = mapped_column(Text)
    mechanism: Mapped[str] = mapped_column(Text)
    example: Mapped[str] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text)
    word_count: Mapped[int] = mapped_column(Integer)
    response_ms: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
