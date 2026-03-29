from datetime import datetime, timedelta, timezone
from uuid import UUID
import traceback

from repositories.explanation_repository import ExplanationRepository
from repositories.quiz_attempt_repository import QuizAttemptRepository
from repositories.quiz_repository import QuizRepository
from repositories.topic_repository import TopicRepository
from schemas.progress import (
    DashboardSummary,
    ProgressHistoryItem,
    ProgressRecommendation,
    ProgressSummary,
)
from services.ai.recommendation_generator import RecommendationGenerator


class ProgressService:
    def __init__(
        self,
        *,
        topic_repo: TopicRepository,
        explanation_repo: ExplanationRepository,
        quiz_repo: QuizRepository,
        attempt_repo: QuizAttemptRepository,
        recommendation_generator: RecommendationGenerator,
    ) -> None:
        self.topic_repo = topic_repo
        self.explanation_repo = explanation_repo
        self.quiz_repo = quiz_repo
        self.attempt_repo = attempt_repo
        self.recommendation_generator = recommendation_generator

    def _parse_session(self, session_id: str) -> UUID:
        if not session_id:
            print("⚠️ PROGRESS: Missing session_id")
            raise ValueError("Missing session_id")

        try:
            return UUID(session_id)
        except Exception:
            print("⚠️ PROGRESS: Invalid session_id:", session_id)
            raise ValueError("Invalid session_id format")

    async def summarize_progress(self, session_id: str) -> ProgressSummary:
        try:
            session_uuid = self._parse_session(session_id)

            topic_count = await self.topic_repo.count_by_session_id(session_uuid)
            attempt_count, average_score = await self.attempt_repo.get_progress_aggregates(session_uuid)

            topic_score = min(topic_count / 20.0, 1.0) * 40
            quiz_score = min(attempt_count / 10.0, 1.0) * 30
            accuracy_score = (average_score / 100.0) * 30

            progress_percent = round(topic_score + quiz_score + accuracy_score, 1)

            if attempt_count == 0:
                return ProgressSummary(
                    topics_studied=topic_count,
                    average_score=0.0,
                    streak_days=0,
                    progress_percent=progress_percent,
                )

            recent_dates = await self.attempt_repo.get_recent_attempt_dates(session_uuid, limit=30)
            streak_days = self._calculate_sql_streak(recent_dates)

            return ProgressSummary(
                topics_studied=topic_count,
                average_score=round(average_score, 2),
                streak_days=streak_days,
                progress_percent=progress_percent,
            )

        except Exception as e:
            print("🔥 PROGRESS SUMMARY ERROR:", str(e))
            traceback.print_exc()
            raise

    async def get_dashboard_summary(self, session_id: str) -> DashboardSummary:
        try:
            session_uuid = self._parse_session(session_id)

            topic_count = await self.topic_repo.count_by_session_id(session_uuid)
            attempt_count, average_score = await self.attempt_repo.get_progress_aggregates(session_uuid)

            total_questions = attempt_count * 5
            history = await self.get_history(session_id, limit=5)

            recent_dates = await self.attempt_repo.get_recent_attempt_dates(session_uuid, limit=30)
            streak = self._calculate_sql_streak(recent_dates)

            performance_trend_rows = await self.attempt_repo.get_performance_trend(session_uuid)
            top_topics_rows = await self.attempt_repo.get_top_topics(session_uuid)

            return DashboardSummary(
                total_topics=topic_count,
                total_questions=total_questions,
                accuracy=round(average_score, 2),
                avg_score=round(average_score, 2),
                streak=streak,
                recent_activity=history,
                performance_trend=performance_trend_rows,
                top_topics=top_topics_rows,
            )

        except Exception as e:
            print("🔥 DASHBOARD ERROR:", str(e))
            traceback.print_exc()
            raise

    async def get_history(
        self, session_id: str, limit: int = 100, offset: int = 0
    ) -> list[ProgressHistoryItem]:
        try:
            session_uuid = self._parse_session(session_id)

            history_rows = await self.attempt_repo.get_history_with_topics(
                session_uuid, limit=limit, offset=offset
            )

            return [
                ProgressHistoryItem(
                    topic=row["topic"],
                    score=float(row["percentage"]),
                    attempted_at=str(row["attempted_at"]),
                )
                for row in history_rows
            ]

        except Exception as e:
            print("🔥 HISTORY ERROR:", str(e))
            traceback.print_exc()
            raise

    async def get_recommendations(
        self, session_id: str
    ) -> list[ProgressRecommendation]:
        try:
            session_uuid = self._parse_session(session_id)

            topics = await self.topic_repo.list_by_session_id(session_uuid, limit=5)
            attempts = await self.attempt_repo.list_by_session_id(session_uuid, limit=3)

            if not topics:
                return []

            studied_topics = [t.normalized_topic for t in topics]

            performance_summary = "User has not taken any quizzes yet."
            if attempts:
                avg_score = sum(float(a.percentage) for a in attempts) / len(attempts)
                performance_summary = (
                    f"User has completed {len(attempts)} quizzes with an average score of {avg_score:.1f}%."
                )

            try:
                output = await self.recommendation_generator.generate(
                    topics=studied_topics,
                    performance_summary=performance_summary,
                )
                return output.recommendations

            except Exception as e:
                print("⚠️ AI RECOMMENDATION FALLBACK:", str(e))
                return [
                    ProgressRecommendation(
                        topic=f"Advanced {studied_topics[0]}",
                        reason="Deepen your understanding of the core concepts.",
                        type="advanced",
                    )
                ]

        except Exception as e:
            print("🔥 RECOMMENDATION ERROR:", str(e))
            traceback.print_exc()
            raise

    def _calculate_sql_streak(self, sorted_dates: list) -> int:
        if not sorted_dates:
            return 0

        streak = 1
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i - 1] - sorted_dates[i]).days == 1:
                streak += 1
            else:
                break

        return streak
        