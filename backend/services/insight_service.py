from uuid import UUID
from api.repositories.topic_repository import TopicRepository
from api.repositories.quiz_attempt_repository import QuizAttemptRepository
from api.services.ai.mentor_tip_generator import MentorTipGenerator
from api.schemas.insight import MentorTipSchema


class InsightService:
    def __init__(
        self,
        *,
        topic_repo: TopicRepository,
        attempt_repo: QuizAttemptRepository,
        mentor_tip_generator: MentorTipGenerator,
    ) -> None:
        self.topic_repo = topic_repo
        self.attempt_repo = attempt_repo
        self.mentor_tip_generator = mentor_tip_generator

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
