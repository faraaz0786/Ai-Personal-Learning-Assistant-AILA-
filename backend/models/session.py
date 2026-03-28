from sqlalchemy import DateTime, JSON, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_active_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
