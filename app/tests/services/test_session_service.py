from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.core.exceptions import AppError
from app.services.session_service import SessionService


def _make_session_model(session_id=None):
    from datetime import datetime, timezone

    model = MagicMock()
    model.id = session_id or uuid4()
    model.created_at = datetime.now(timezone.utc)
    model.last_active_at = datetime.now(timezone.utc)
    return model


@pytest.mark.asyncio
async def test_session_service_creates_and_fetches_session() -> None:
    mock_repo = MagicMock()
    created = _make_session_model()
    mock_repo.create = AsyncMock(return_value=created)
    updated = _make_session_model(session_id=created.id)
    mock_repo.get_by_id = AsyncMock(return_value=created)
    mock_repo.update_last_active = AsyncMock(return_value=updated)

    service = SessionService(session_repo=mock_repo)

    session = await service.create_session()
    fetched = await service.get_session(session.session_id)

    assert fetched.session_id == session.session_id
    assert fetched.last_active_at >= session.last_active_at


@pytest.mark.asyncio
async def test_session_service_rejects_invalid_cookie_value() -> None:
    mock_repo = MagicMock()
    service = SessionService(session_repo=mock_repo)

    with pytest.raises(AppError) as exc:
        await service.require_session("not-a-uuid")

    assert exc.value.code == "SESSION_MISMATCH"


@pytest.mark.asyncio
async def test_session_service_rejects_mismatched_access() -> None:
    mock_repo = MagicMock()
    created = _make_session_model()
    mock_repo.create = AsyncMock(return_value=created)
    mock_repo.get_by_id = AsyncMock(return_value=created)
    mock_repo.update_last_active = AsyncMock(return_value=created)

    service = SessionService(session_repo=mock_repo)

    session = await service.create_session()

    with pytest.raises(AppError) as exc:
        await service.assert_session_access(
            cookie_session_id=str(uuid4()),
            resource_session_id=session.session_id,
        )

    assert exc.value.code == "SESSION_MISMATCH"
