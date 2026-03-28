from uuid import uuid4

from core.dependencies import get_ai_service, get_session_service
from schemas.learn import ExplainRequest, ExplainResponse


class FakeAIService:
    async def explain(self, payload: ExplainRequest, session_id: str) -> ExplainResponse:
        _ = session_id
        return ExplainResponse.placeholder(topic=payload.topic)


class FakeSessionService:
    def __init__(self) -> None:
        self.session_id = uuid4()

    async def require_session(self, session_id: str | None):
        _ = session_id
        return self.session_id


def test_explain_endpoint_returns_documented_shape(client) -> None:
    fake_session_service = FakeSessionService()
    client.app.dependency_overrides[get_ai_service] = lambda: FakeAIService()
    client.app.dependency_overrides[get_session_service] = lambda: fake_session_service

    response = client.post(
        "/api/v1/learn/explain",
        json={"topic": "Photosynthesis", "subject": "Science"},
        cookies={"aila_session": str(fake_session_service.session_id)},
    )

    client.app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert "topic_id" in data
    assert "explanation" in data
    assert "summary" in data


def test_explain_endpoint_returns_structured_validation_error(client) -> None:
    fake_session_service = FakeSessionService()
    client.app.dependency_overrides[get_session_service] = lambda: fake_session_service
    response = client.post(
        "/api/v1/learn/explain",
        json={"topic": "a", "subject": "Science"},
        cookies={"aila_session": str(fake_session_service.session_id)},
    )

    client.app.dependency_overrides.clear()
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "TOPIC_TOO_SHORT"
