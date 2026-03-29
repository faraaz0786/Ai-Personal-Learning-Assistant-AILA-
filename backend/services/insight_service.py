from uuid import UUID
from repositories.topic_repository import TopicRepository
from repositories.quiz_attempt_repository import QuizAttemptRepository
from services.ai.mentor_tip_generator import MentorTipGenerator
from services.ai.insight_generator import InsightGenerator
from schemas.insight import MentorTipSchema, QuizInsightSchema


class InsightService:
    def __init__(
        self,
        *,
        topic_repo: TopicRepository,
        attempt_repo: QuizAttemptRepository,
        mentor_tip_generator: MentorTipGenerator,
        insight_generator: InsightGenerator,
    ) -> None:
        self.topic_repo = topic_repo
        self.attempt_repo = attempt_repo
        self.mentor_tip_generator = mentor_tip_generator
        self.insight_generator = insight_generator

    async def get_mentor_tip(self, session_id: str) -> MentorTipSchema:
        topics = await self.topic_repo.list_by_session_id(UUID(session_id), limit=1)
        if not topics:
            return MentorTipSchema(
                tip="Welcome to your scholarly workspace! Start by exploring a topic.",
                focus_area="Initialization",
                recommendation="Enter a topic in the search bar above.",
            )

        current_topic = topics[0].normalized_topic
        attempt_count, average_score = await self.attempt_repo.get_progress_aggregates(
            UUID(session_id)
        )

        recent_history = await self.attempt_repo.get_recent_attempt_dates(
            UUID(session_id), limit=5
        )
        history_desc = f"User has studied {len(topics)} topics and completed {attempt_count} quizzes."

        return await self.mentor_tip_generator.generate(
            topic=current_topic,
            accuracy=average_score,
            recent_activity=history_desc,
        )

    async def generate_quiz_insights(
        self, topic_id: UUID, score: int, total: int
    ) -> QuizInsightSchema:
        topic_model = await self.topic_repo.get_by_id(topic_id)
        if not topic_model:
            # Fallback for robustness
            return QuizInsightSchema(
                feedback="Excellent effort! Keep pushing your boundaries.",
                focus_area="Review",
                next_steps="Review the core concepts and try again."
            )

        accuracy = (score / total) * 100 if total > 0 else 0
        return await self.insight_generator.generate(
            topic=topic_model.normalized_topic,
            score=score,
            total=total,
            accuracy=accuracy
        )
