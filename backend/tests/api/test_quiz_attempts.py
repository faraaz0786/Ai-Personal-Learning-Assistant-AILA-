from uuid import uuid4

from app.core.dependencies import get_quiz_service, get_session_service
from app.schemas.learn import QuizQuestion
from app.schemas.quiz import QuizAttemptResponse, QuizDetailResponse


class FakeQuizService:
    def __init__(self) -> None:
        self.quiz_id = uuid4()
        self.topic_id = uuid4()

    def get_quiz(self, quiz_id, session_id):
        _ = session_id
        return QuizDetailResponse(
            quiz_id=quiz_id,
            topic_id=self.topic_id,
            questions=[
                QuizQuestion(
                    id=1,
                    question="What is gravity in simple physics terms?",
                    options=["A force", "A cell", "A language", "A planet"],
                    correct_index=0,
                    explanation="Gravity is a force that attracts masses toward each other.",
                )
            ],
        )

    def submit_attempt(self, quiz_id, answers, session_id):
        _ = (quiz_id, session_id)
        return QuizAttemptResponse(
            attempt_id=uuid4(),
            score=1,
            max_score=1,
            percentage=100.0,
            results=[
                {
                    "question_id": 1,
                    "correct": True,
                    "your_answer": answers[0],
                    "correct_index": 0,
                }
            ],
        )

    def list_attempts(self, quiz_id, session_id):
        _ = (quiz_id, session_id)
        return []


class FakeSessionService:
    def __init__(self) -> None:
        self.session_id = uuid4()

    async def require_session(self, session_id: str | None):
        _ = session_id
        return self.session_id


def test_submit_quiz_attempt_returns_documented_shape(client) -> None:
    fake_service = FakeQuizService()
    fake_session_service = FakeSessionService()
    client.app.dependency_overrides[get_quiz_service] = lambda: fake_service
    client.app.dependency_overrides[get_session_service] = lambda: fake_session_service

    response = client.post(
        f"/api/v1/quizzes/{fake_service.quiz_id}/attempts",
        json={"answers": [0]},
        cookies={"aila_session": str(fake_session_service.session_id)},
    )

    client.app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 1
    assert data["max_score"] == 1
    assert len(data["results"]) == 1
