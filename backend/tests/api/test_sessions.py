from app.core.dependencies import get_session_service


class FakeSessionService:
    def __init__(self) -> None:
        self.created = None

    async def create_session(self):
        from app.schemas.session import SessionResponse

        self.created = SessionResponse.placeholder()
        return self.created

    async def assert_session_access(self, cookie_session_id, resource_session_id):
        _ = (cookie_session_id, resource_session_id)
        return resource_session_id

    async def get_session(self, session_id):
        return self.created if self.created else __import__(
            "app.schemas.session", fromlist=["SessionResponse"]
        ).SessionResponse.placeholder(session_id=session_id)

    async def delete_session(self, session_id):
        _ = session_id
        return None


def test_create_session_sets_cookie(client) -> None:
    fake_service = FakeSessionService()
    client.app.dependency_overrides[get_session_service] = lambda: fake_service

    response = client.post("/api/v1/sessions")

    client.app.dependency_overrides.clear()

    assert response.status_code == 201
    assert "aila_session" in response.headers.get("set-cookie", "")


def test_delete_session_returns_no_content(client) -> None:
    fake_service = FakeSessionService()
    created = client.post("/api/v1/sessions")
    session_id = created.json()["id"]
    client.app.dependency_overrides[get_session_service] = lambda: fake_service

    response = client.delete(
        f"/api/v1/sessions/{session_id}",
        cookies={"aila_session": session_id},
    )

    client.app.dependency_overrides.clear()

    assert response.status_code == 204
