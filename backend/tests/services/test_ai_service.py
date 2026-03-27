from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.schemas.learn import ExplainRequest
from app.services.ai.explanation_generator import ExplanationGenerator
from app.services.ai.quiz_generator import QuizGenerator
from app.services.ai.summary_generator import SummaryGenerator
from app.services.ai_service import AIService
from app.services.cache.ai_cache_service import AICacheService
from app.services.prompt_service import PromptService
from app.services.quiz_service import QuizService
from app.services.response_parser import ResponseParser
from app.services.session_service import SessionService


class StubProvider:
    def __init__(self) -> None:
        self.responses = [
            (
                '{"definition":"Photosynthesis is the process plants use to convert '
                'light energy into chemical energy for growth and survival.",'
                '"mechanism":"Plants absorb sunlight through chlorophyll, take in '
                'carbon dioxide and water, and transform them into glucose and oxygen '
                'through linked chemical reactions in the chloroplast.",'
                '"example":"A green leaf on a sunflower produces glucose from sunlight, '
                'water, and carbon dioxide, helping the plant store usable energy."}'
            ),
            (
                '{"summary":"Photosynthesis allows plants to capture sunlight and turn '
                'it into stored chemical energy. The process mainly happens in '
                'chloroplasts, where water and carbon dioxide are converted into glucose '
                'and oxygen. This supports plant growth and also supplies oxygen to the '
                'atmosphere. It is one of the core biological processes that sustains '
                'most life on Earth, and it also forms the energy foundation for many '
                'food chains studied in biology."}'
            ),
        ]

    async def complete(self, **_: object) -> str:
        return self.responses.pop(0)


class StubPromptService(PromptService):
    def __init__(self) -> None:
        pass

    def render(self, template_name: str, **context: object) -> str:
        return f"{template_name}:{context}"

    def get_system_prompt(self) -> str:
        return "system"


def _make_session_model(session_id=None):
    from datetime import datetime, timezone

    model = MagicMock()
    model.id = session_id or uuid4()
    model.created_at = datetime.now(timezone.utc)
    model.last_active_at = datetime.now(timezone.utc)
    return model


def _make_topic_model(topic_id, session_id):
    model = MagicMock()
    model.id = topic_id
    model.session_id = session_id
    model.raw_input = "Photosynthesis"
    model.normalized_topic = "Photosynthesis"
    model.subject = "General"
    model.llm_model = "gpt-4o"
    model.cached = False
    return model


@pytest.mark.asyncio
async def test_ai_service_generates_explanation_and_summary() -> None:
    prompt_service = StubPromptService()
    provider = StubProvider()
    response_parser = ResponseParser()

    session_id = uuid4()
    session_model = _make_session_model(session_id)

    # Mock session repo
    session_repo = MagicMock()
    session_repo.create = AsyncMock(return_value=session_model)
    session_repo.get_by_id = AsyncMock(return_value=session_model)
    session_repo.update_last_active = AsyncMock(return_value=session_model)

    # Mock topic repo
    topic_id = uuid4()
    topic_model = _make_topic_model(topic_id, session_id)
    topic_repo = MagicMock()
    topic_repo.create = AsyncMock(return_value=topic_model)

    # Mock explanation repo
    explanation_model = MagicMock()
    explanation_model.id = uuid4()
    explanation_repo = MagicMock()
    explanation_repo.create = AsyncMock(return_value=explanation_model)

    # Mock quiz-related repos
    quiz_repo = MagicMock()
    attempt_repo = MagicMock()

    session_service = SessionService(session_repo=session_repo)
    quiz_service = QuizService(quiz_repo=quiz_repo, attempt_repo=attempt_repo, topic_repo=topic_repo)

    model_name = "gpt-4o"
    service = AIService(
        quiz_service=quiz_service,
        session_service=session_service,
        explanation_generator=ExplanationGenerator(
            prompt_service=prompt_service,
            provider=provider,
            response_parser=response_parser,
            system_prompt=prompt_service.get_system_prompt(),
            model=model_name,
        ),
        summary_generator=SummaryGenerator(
            prompt_service=prompt_service,
            provider=provider,
            response_parser=response_parser,
            system_prompt=prompt_service.get_system_prompt(),
            model=model_name,
        ),
        quiz_generator=QuizGenerator(
            prompt_service=prompt_service,
            provider=provider,
            response_parser=response_parser,
            system_prompt=prompt_service.get_system_prompt(),
            model=model_name,
        ),
        topic_repo=topic_repo,
        explanation_repo=explanation_repo,
        cache_service=AICacheService(),
    )

    # Create session first
    session = await session_service.create_session()
    response = await service.explain(
        ExplainRequest(topic="Photosynthesis"),
        str(session.session_id),
    )

    assert response.normalized_topic == "Photosynthesis"
    assert response.explanation.definition
    assert response.summary
    assert 60 <= len(response.summary.split()) <= 100
