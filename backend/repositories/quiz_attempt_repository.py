from collections.abc import Sequence
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import desc

from models.quiz_attempt import QuizAttemptModel
from repositories.base import BaseRepository


class QuizAttemptRepository(BaseRepository[QuizAttemptModel]):
    async def create(
        self,
        *,
        quiz_id: UUID,
        session_id: UUID,
        answers: list[int],
        score: int,
        max_score: int,
        percentage: float,
        time_taken_sec: int | None = None,
    ) -> QuizAttemptModel:
        attempt = QuizAttemptModel(
            id=uuid4(),
            quiz_id=quiz_id,
            session_id=session_id,
            answers=answers,
            score=score,
            max_score=max_score,
            percentage=Decimal(str(percentage)),
            time_taken_sec=time_taken_sec,
        )
        return await self.add(attempt)

    async def get_by_id(self, attempt_id: UUID) -> QuizAttemptModel | None:
        statement = self.select_model(QuizAttemptModel).where(QuizAttemptModel.id == attempt_id)
        return await self.execute_one_or_none(statement)

    async def list_by_quiz_id(
        self, quiz_id: UUID, limit: int = 100, offset: int = 0
    ) -> Sequence[QuizAttemptModel]:
        statement = (
            self.select_model(QuizAttemptModel)
            .where(QuizAttemptModel.quiz_id == quiz_id)
            .order_by(desc(QuizAttemptModel.attempted_at))
            .limit(limit)
            .offset(offset)
        )
        return await self.execute_all(statement)

    async def list_by_session_id(
        self, session_id: UUID, limit: int = 100, offset: int = 0
    ) -> Sequence[QuizAttemptModel]:
        statement = (
            self.select_model(QuizAttemptModel)
            .where(QuizAttemptModel.session_id == session_id)
            .order_by(desc(QuizAttemptModel.attempted_at))
            .limit(limit)
            .offset(offset)
        )
        return await self.execute_all(statement)

    async def get_history_with_topics(
        self, session_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[dict]:
        from sqlalchemy import select
        from models.quiz import QuizModel
        from models.topic import TopicModel
        statement = (
            select(
                QuizAttemptModel.percentage,
                QuizAttemptModel.attempted_at,
                TopicModel.normalized_topic
            )
            .join(QuizModel, QuizAttemptModel.quiz_id == QuizModel.id)
            .join(TopicModel, QuizModel.topic_id == TopicModel.id)
            .where(QuizAttemptModel.session_id == session_id)
            .order_by(desc(QuizAttemptModel.attempted_at))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(statement)
        return [
            {"percentage": row.percentage, "attempted_at": row.attempted_at, "topic": row.normalized_topic}
            for row in result
        ]

    async def get_progress_aggregates(self, session_id: UUID) -> tuple[int, float]:
        """Returns (attempt_count, average_percentage) using SQL aggregation."""
        from sqlalchemy import select, func
        statement = select(
            func.count(QuizAttemptModel.id),
            func.avg(QuizAttemptModel.percentage)
        ).where(QuizAttemptModel.session_id == session_id)
        result = await self.session.execute(statement)
        row = result.first()
        if not row:
            return 0, 0.0
        count = row[0] or 0
        avg = float(row[1]) if row[1] is not None else 0.0
        return count, avg

    async def get_recent_attempt_dates(self, session_id: UUID, limit: int = 7) -> list:
        """Returns distinct dates of recent attempts for streak calculation."""
        from sqlalchemy import select, func
        statement = (
            select(func.date(QuizAttemptModel.attempted_at).label('attempt_date'))
            .where(QuizAttemptModel.session_id == session_id)
            .where(QuizAttemptModel.attempted_at.is_not(None))
            .group_by('attempt_date')
            .order_by(desc('attempt_date'))
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return [row[0] for row in result]

    async def get_performance_trend(self, session_id: UUID, limit: int = 7) -> list[dict]:
        """Returns daily average scores for trend visualization."""
        from sqlalchemy import select, func
        statement = (
            select(
                func.date(QuizAttemptModel.attempted_at).label('date'),
                func.avg(QuizAttemptModel.percentage).label('avg_score')
            )
            .where(QuizAttemptModel.session_id == session_id)
            .group_by('date')
            .order_by('date')
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return [{"date": str(row.date), "score": float(row.avg_score)} for row in result]

    async def get_top_topics(self, session_id: UUID, limit: int = 5) -> list[dict]:
        """Returns top performing topics based on average quiz scores."""
        from sqlalchemy import select, func
        from models.quiz import QuizModel
        from models.topic import TopicModel
        statement = (
            select(
                TopicModel.normalized_topic.label('topic'),
                func.avg(QuizAttemptModel.percentage).label('avg_score')
            )
            .join(QuizModel, QuizAttemptModel.quiz_id == QuizModel.id)
            .join(TopicModel, QuizModel.topic_id == TopicModel.id)
            .where(QuizAttemptModel.session_id == session_id)
            .group_by(TopicModel.normalized_topic)
            .order_by(desc('avg_score'))
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return [{"topic": row.topic, "score": float(row.avg_score)} for row in result]
