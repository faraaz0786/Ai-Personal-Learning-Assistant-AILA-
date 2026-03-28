from collections.abc import Sequence
from uuid import UUID, uuid4

from sqlalchemy import desc

from models.topic import TopicModel
from repositories.base import BaseRepository


class TopicRepository(BaseRepository[TopicModel]):
    async def create(
        self,
        *,
        session_id: UUID,
        raw_input: str,
        normalized_topic: str,
        subject: str | None,
        llm_model: str,
        cached: bool = False,
    ) -> TopicModel:
        topic = TopicModel(
            id=uuid4(),
            session_id=session_id,
            raw_input=raw_input,
            normalized_topic=normalized_topic,
            subject=subject,
            llm_model=llm_model,
            cached=cached,
        )
        return await self.add(topic)

    async def get_by_id(self, topic_id: UUID) -> TopicModel | None:
        statement = self.select_model(TopicModel).where(TopicModel.id == topic_id)
        return await self.execute_one_or_none(statement)

    async def list_by_session_id(
        self, session_id: UUID, limit: int = 100, offset: int = 0
    ) -> Sequence[TopicModel]:
        statement = (
            self.select_model(TopicModel)
            .where(TopicModel.session_id == session_id)
            .order_by(desc(TopicModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return await self.execute_all(statement)

    async def count_by_session_id(self, session_id: UUID) -> int:
        from sqlalchemy import select, func
        from core.timing import timing_tracker
        
        statement = select(func.count(TopicModel.id)).where(TopicModel.session_id == session_id)
        with timing_tracker.measure("db"):
            result = await self.session.execute(statement)
            count = result.scalar_one_or_none()
            return count or 0

    async def get_by_session_and_normalized_topic(
        self, *, session_id: UUID, normalized_topic: str
    ) -> TopicModel | None:
        statement = self.select_model(TopicModel).where(
            TopicModel.session_id == session_id,
            TopicModel.normalized_topic == normalized_topic,
        )
        return await self.execute_one_or_none(statement)
