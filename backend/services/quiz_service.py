from uuid import UUID, uuid4

from api.core.exceptions import AppError
from api.repositories.quiz_repository import QuizRepository
from api.repositories.quiz_attempt_repository import QuizAttemptRepository
from api.repositories.topic_repository import TopicRepository
from api.schemas.learn import QuizQuestion, QuizResponse
from api.schemas.quiz import QuizAttemptResponse, QuizAttemptResult, QuizDetailResponse
from api.services.progress_service import ProgressService
from api.services.insight_service import InsightService


class QuizService:
    """Validates, stores, and scores generated quizzes."""

    def __init__(
        self,
        *,
        quiz_repo: QuizRepository,
        attempt_repo: QuizAttemptRepository,
        topic_repo: TopicRepository,
        progress_service: ProgressService,
        insight_service: InsightService,
    ) -> None:
        self.quiz_repo = quiz_repo
        self.attempt_repo = attempt_repo
        self.topic_repo = topic_repo
        self.progress_service = progress_service
        self.insight_service = insight_service

    async def create_quiz(
        self,
        *,
        topic_id: UUID,
        questions: list[QuizQuestion],
        expected_count: int,
        session_id: str,
        difficulty: str = "medium",
    ) -> QuizResponse:
        if len(questions) != expected_count:
            raise AppError(
                status_code=503,
                code="LLM_UNAVAILABLE",
                message="Generated quiz question count did not match the request.",
                details={"expected_count": expected_count, "actual_count": len(questions)},
            )

        questions_dicts = [q.model_dump() for q in questions]
        model = await self.quiz_repo.create(
            topic_id=topic_id,
            questions=questions_dicts,
            question_count=expected_count,
            difficulty=difficulty,
        )

        return QuizResponse(
            quiz_id=model.id,
            topic_id=model.topic_id,
            questions=questions,
        )

    async def get_quiz(self, quiz_id: UUID, session_id: str) -> QuizDetailResponse:
        quiz = await self.quiz_repo.get_by_id(quiz_id)
        if quiz is None:
            raise AppError(
                status_code=404,
                code="QUIZ_NOT_FOUND",
                message="The requested quiz could not be found.",
            )

        topic = await self.topic_repo.get_by_id(quiz.topic_id)
        if topic is None or str(topic.session_id) != session_id:
            raise AppError(
                status_code=403,
                code="SESSION_MISMATCH",
                message="The requested resource belongs to a different session.",
            )

        questions = [QuizQuestion.model_validate(q) for q in quiz.questions]
        return QuizDetailResponse(
            quiz_id=quiz.id,
            topic_id=quiz.topic_id,
            questions=questions,
        )

    async def submit_attempt(
        self, quiz_id: UUID, answers: list[int], session_id: str
    ) -> QuizAttemptResponse:
        quiz = await self.quiz_repo.get_by_id(quiz_id)
        if quiz is None:
            raise AppError(
                status_code=404,
                code="QUIZ_NOT_FOUND",
                message="The requested quiz could not be found.",
            )

        topic = await self.topic_repo.get_by_id(quiz.topic_id)
        if topic is None or str(topic.session_id) != session_id:
            raise AppError(
                status_code=403,
                code="SESSION_MISMATCH",
                message="The requested resource belongs to a different session.",
            )

        questions = [QuizQuestion.model_validate(q) for q in quiz.questions]
        if len(answers) != len(questions):
            raise AppError(
                status_code=422,
                code="ANSWER_COUNT_MISMATCH",
                message="answers array length does not match quiz question count.",
                details={
                    "expected_count": len(questions),
                    "actual_count": len(answers),
                },
            )

        results: list[QuizAttemptResult] = []
        score = 0

        for index, question in enumerate(questions):
            your_answer = answers[index]
            correct = your_answer == question.correct_index
            if correct:
                score += 1
            results.append(
                QuizAttemptResult(
                    question_id=question.id,
                    correct=correct,
                    your_answer=your_answer,
                    correct_index=question.correct_index,
                )
            )

        max_score = len(questions)
        percentage = round((score / max_score) * 100, 2)

        attempt_model = await self.attempt_repo.create(
            quiz_id=quiz_id,
            session_id=UUID(session_id),
            answers=answers,
            score=score,
            max_score=max_score,
            percentage=percentage,
        )

        # 5. Fetch updated dashboard analytics for immediate feedback
        analytics = await self.progress_service.get_dashboard_summary(session_id)

        # 6. Generate AI Insights for this specific attempt
        insights = await self.insight_service.generate_quiz_insights(
            topic_id=quiz.topic_id,
            score=score,
            total=len(quiz.questions)
        )

        return QuizAttemptResponse(
            attempt_id=attempt_model.id,
            score=score,
            max_score=len(quiz.questions),
            percentage=percentage,
            results=results,
            analytics=analytics,
            insights=insights
        )

    async def list_attempts(
        self, quiz_id: UUID, session_id: str, limit: int = 100, offset: int = 0
    ) -> list[QuizAttemptResponse]:
        quiz = await self.quiz_repo.get_by_id(quiz_id)
        if quiz is None:
            raise AppError(
                status_code=404,
                code="QUIZ_NOT_FOUND",
                message="The requested quiz could not be found.",
            )

        topic = await self.topic_repo.get_by_id(quiz.topic_id)
        if topic is None or str(topic.session_id) != session_id:
            raise AppError(
                status_code=403,
                code="SESSION_MISMATCH",
                message="The requested resource belongs to a different session.",
            )

        models = await self.attempt_repo.list_by_quiz_id(quiz_id, limit=limit, offset=offset)
        questions = [QuizQuestion.model_validate(q) for q in quiz.questions]

        responses: list[QuizAttemptResponse] = []
        for m in models:
            results: list[QuizAttemptResult] = []
            for index, question in enumerate(questions):
                your_answer = m.answers[index] if index < len(m.answers) else -1
                results.append(
                    QuizAttemptResult(
                        question_id=question.id,
                        correct=your_answer == question.correct_index,
                        your_answer=your_answer,
                        correct_index=question.correct_index,
                    )
                )
            responses.append(
                QuizAttemptResponse(
                    attempt_id=m.id,
                    score=m.score,
                    max_score=m.max_score,
                    percentage=float(m.percentage),
                    results=results,
                )
            )
        return responses

    async def list_attempts_for_session(
        self, session_id: str
    ) -> list[tuple[UUID, float, str]]:
        """Return (topic_id, percentage, attempted_at) tuples for a session."""
        models = await self.attempt_repo.list_by_session_id(UUID(session_id))
        items: list[tuple[UUID, float, str]] = []
        for m in models:
            quiz = await self.quiz_repo.get_by_id(m.quiz_id)
            if quiz is not None:
                items.append((quiz.topic_id, float(m.percentage), str(m.attempted_at)))
        return items
