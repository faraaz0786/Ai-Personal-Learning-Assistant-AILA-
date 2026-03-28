from uuid import UUID
from api.repositories.topic_repository import TopicRepository
from api.repositories.explanation_repository import ExplanationRepository
from api.schemas.library import LibraryItem, LibraryResponse


class LibraryService:
    def __init__(
        self,
        *,
        topic_repo: TopicRepository,
        explanation_repo: ExplanationRepository,
    ) -> None:
        self.topic_repo = topic_repo
        self.explanation_repo = explanation_repo

    async def get_library(
        self, session_id: str, limit: int = 100, offset: int = 0
    ) -> LibraryResponse:
        topics = await self.topic_repo.list_by_session_id(
            UUID(session_id), limit=limit, offset=offset
        )
        items = []
        for topic in topics:
            explanation = await self.explanation_repo.get_by_topic_id(topic.id)
            items.append(
                LibraryItem(
                    id=topic.id,
                    topic=topic.normalized_topic,
                    summary=explanation.summary if explanation else "No summary available",
                    created_at=topic.created_at,
                    last_accessed=topic.created_at, # Placeholder for now
                )
            )
        
        total_count = await self.topic_repo.count_by_session_id(UUID(session_id))
        return LibraryResponse(items=items, total_count=total_count)
