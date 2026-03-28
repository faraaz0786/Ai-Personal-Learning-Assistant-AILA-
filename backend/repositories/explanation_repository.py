from uuid import UUID, uuid4

from sqlalchemy import delete

from models.explanation import ExplanationModel
from repositories.base import BaseRepository


class ExplanationRepository(BaseRepository[ExplanationModel]):
    async def create(
        self,
        *,
        topic_id: UUID,
        definition: str,
        mechanism: str,
        example: str,
        summary: str,
        word_count: int,
        response_ms: int,
    ) -> ExplanationModel:
        explanation = ExplanationModel(
            id=uuid4(),
            topic_id=topic_id,
            definition=definition,
            mechanism=mechanism,
            example=example,
            summary=summary,
            word_count=word_count,
            response_ms=response_ms,
        )
        return await self.add(explanation)

    async def get_by_topic_id(self, topic_id: UUID) -> ExplanationModel | None:
        statement = self.select_model(ExplanationModel).where(
            ExplanationModel.topic_id == topic_id
        )
        return await self.execute_one_or_none(statement)

    async def delete_by_topic_id(self, topic_id: UUID) -> None:
        await self.session.execute(
            delete(ExplanationModel).where(ExplanationModel.topic_id == topic_id)
        )
        await self.session.flush()
