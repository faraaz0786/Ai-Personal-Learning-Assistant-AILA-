from uuid import uuid4

from core.dependencies import get_progress_service, get_session_service
from schemas.progress import ProgressHistoryItem, ProgressRecommendation, ProgressSummary


class FakeSessionService:
    def __init__(self) -> None:
        self.session_id = uuid4()

    async def require_session(self, session_id: str | None):
        _ = session_id
        return self.session_id


class FakeProgressService:
    async def summarize_progress(self, session_id: str) -> ProgressSummary:
        _ = session_id
        return ProgressSummary(topics_studied=2, average_score=75.0, streak_days=2)

    async def get_history(self, session_id: str) -> list[ProgressHistoryItem]:
        _ = session_id
        return [
            ProgressHistoryItem(
                topic="Photosynthesis",
                score=80.0,
                attempted_at="2026-03-20T00:00:00+00:00",
            )
        ]

    async def get_recommendations(self, session_id: str) -> list[ProgressRecommendation]:
        _ = session_id
        return [
            ProgressRecommendation(
                topic="Advanced Photosynthesis",
                reason="Good performance suggests moving forward.",
                type="advanced",
            )
        ]


def test_progress_summary_endpoint_returns_data(client) -> None:
    client.app.dependency_overrides[get_progress_service] = lambda: FakeProgressService()
    client.app.dependency_overrides[get_session_service] = lambda: FakeSessionService()

    response = client.get("/api/v1/progress/summary", cookies={"aila_session": str(uuid4())})

    client.app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["topics_studied"] == 2


def test_progress_recommendations_endpoint_returns_list(client) -> None:
    client.app.dependency_overrides[get_progress_service] = lambda: FakeProgressService()
    client.app.dependency_overrides[get_session_service] = lambda: FakeSessionService()

    response = client.get(
        "/api/v1/progress/recommendations",
        cookies={"aila_session": str(uuid4())},
    )

    client.app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()[0]["type"] == "advanced"
