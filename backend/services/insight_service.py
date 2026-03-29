from uuid import UUID
import traceback

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

    def _parse_session(self, session_id: str) -> UUID:
        if not session_id:
            print("⚠️ INSIGHT: Missing session_id")
            raise ValueError("Missing session_id")

        try:
            return UUID(session_id)
        except Exception:
            print("⚠️ INSIGHT: Invalid session_id:", session_id)
            raise ValueError("Invalid session_id format")

    async def get_mentor_tip(self, session_id: str) -> MentorTipSchema:
        try:
            session_uuid = self._parse_session(session_id)

            topics = await self.topic_repo.list_by_session_id(session_uuid, limit=1)

            if not topics:
                return MentorTipSchema(
                    tip="Welcome to your scholarly workspace! Start by exploring a topic.",
                    focus_area="Initialization",
                    recommendation="Enter a topic in the search bar above.",
                )

            current_topic = topics[0].normalized_topic

            attempt_count, average_score = await self.attempt_repo.get_progress_aggregates(
                session_uuid
            )

            history_desc = (
                f"User has studied {len(topics)} topics and completed {attempt_count} quizzes."
            )

            return await self.mentor_tip_generator.generate(
                topic=current_topic,
                accuracy=average_score,
                recent_activity=history_desc,
            )

        except Exception as e:
            print("🔥 MENTOR TIP ERROR:", str(e))
            traceback.print_exc()
            raise

    async def generate_quiz_insights(
        self, topic_id: UUID, score: int, total: int
    ) -> QuizInsightSchema:
        try:
            topic_model = await self.topic_repo.get_by_id(topic_id)

            if not topic_model:
                return QuizInsightSchema(
                    feedback="Excellent effort! Keep pushing your boundaries.",
                    focus_area="Review",
                    next_steps="Review the core concepts and try again.",
                )

            accuracy = (score / total) * 100 if total > 0 else 0

            return await self.insight_generator.generate(
                topic=topic_model.normalized_topic,
                score=score,
                total=total,
                accuracy=accuracy,
            )

        except Exception as e:
            print("🔥 QUIZ INSIGHT ERROR:", str(e))
            traceback.print_exc()
            raise
        