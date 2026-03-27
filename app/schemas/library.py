from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class LibraryItem(BaseModel):
    id: UUID
    topic: str
    summary: str
    created_at: datetime
    last_accessed: datetime | None = None

class LibraryResponse(BaseModel):
    items: list[LibraryItem]
    total_count: int
