from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.progress_service import ProgressService


def _make_topic_model(normalized_topic="Photosynthesis"):
    model = MagicMock()
    model.id = uuid4()
    model.normalized_topic = normalized_topic
    return model


def _make_attempt_model(quiz_id, percentage=80.0):
    from datetime import datetime, timezone

    model = MagicMock()
    model.id = uuid4()
    model.quiz_id = quiz_id
    model.percentage = percentage
    model.attempted_at = datetime.now(timezone.utc)
    return model


def _make_quiz_model(topic_id):
    model = MagicMock()
    model.id = uuid4()
    model.topic_id = topic_id
    return model


@pytest.mark.asyncio
async def test_progress_service_summarizes_attempts() -> None:
    topic = _make_topic_model()
    quiz = _make_quiz_model(topic.id)
    attempt = _make_attempt_model(quiz.id, percentage=80.0)

    topic_repo = MagicMock()
    topic_repo.list_by_session_id = AsyncMock(return_value=[topic])
    topic_repo.get_by_id = AsyncMock(return_value=topic)

    explanation_repo = MagicMock()
    quiz_repo = MagicMock()
    quiz_repo.get_by_id = AsyncMock(return_value=quiz)

    attempt_repo = MagicMock()
    attempt_repo.list_by_session_id = AsyncMock(return_value=[attempt])

    service = ProgressService(
        topic_repo=topic_repo,
        explanation_repo=explanation_repo,
        quiz_repo=quiz_repo,
        attempt_repo=attempt_repo,
    )

    summary = await service.summarize_progress("session-1")

    assert summary.topics_studied == 1
    assert summary.average_score == 80.0


@pytest.mark.asyncio
async def test_progress_service_returns_advanced_recommendations_for_high_score() -> None:
    topic = _make_topic_model()
    quiz = _make_quiz_model(topic.id)
    attempt = _make_attempt_model(quiz.id, percentage=92.0)

    topic_repo = MagicMock()
    topic_repo.list_by_session_id = AsyncMock(return_value=[topic])

    explanation_repo = MagicMock()
    quiz_repo = MagicMock()

    attempt_repo = MagicMock()
    attempt_repo.list_by_session_id = AsyncMock(return_value=[attempt])

    service = ProgressService(
        topic_repo=topic_repo,
        explanation_repo=explanation_repo,
        quiz_repo=quiz_repo,
        attempt_repo=attempt_repo,
    )

    recommendations = await service.get_recommendations("session-1")

    assert len(recommendations) == 3
    assert recommendations[0].type == "advanced"
