from collections.abc import Sequence
from uuid import UUID, uuid4

from sqlalchemy import desc

from app.models.quiz import QuizModel
from app.repositories.base import BaseRepository


class QuizRepository(BaseRepository[QuizModel]):
    async def create(
        self,
        *,
        topic_id: UUID,
        questions: list[dict],
        question_count: int,
        difficulty: str,
    ) -> QuizModel:
        quiz = QuizModel(
            id=uuid4(),
            topic_id=topic_id,
            questions=questions,
            question_count=question_count,
            difficulty=difficulty,
        )
        return await self.add(quiz)

    async def get_by_id(self, quiz_id: UUID) -> QuizModel | None:
        statement = self.select_model(QuizModel).where(QuizModel.id == quiz_id)
        return await self.execute_one_or_none(statement)

    async def list_by_topic_id(self, topic_id: UUID) -> Sequence[QuizModel]:
        statement = (
            self.select_model(QuizModel)
            .where(QuizModel.topic_id == topic_id)
            .order_by(desc(QuizModel.created_at))
        )
        return await self.execute_all(statement)

    async def list_by_session_id(self, session_id: UUID) -> Sequence[QuizModel]:
        from app.models.topic import TopicModel

        statement = (
            self.select_model(QuizModel)
            .join(TopicModel, QuizModel.topic_id == TopicModel.id)
            .where(TopicModel.session_id == session_id)
            .order_by(desc(QuizModel.created_at))
        )
        return await self.execute_all(statement)
