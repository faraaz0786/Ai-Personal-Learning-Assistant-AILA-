from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SessionResponse(BaseModel):
    session_id: UUID = Field(alias="id")
    created_at: datetime
    last_active_at: datetime

    @classmethod
    def placeholder(cls, session_id: UUID | None = None) -> "SessionResponse":
        now = datetime.now(timezone.utc)
        return cls(id=session_id or uuid4(), created_at=now, last_active_at=now)
