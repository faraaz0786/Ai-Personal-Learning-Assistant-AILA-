from functools import lru_cache
from pathlib import Path

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.config import Settings, get_settings
from api.core.rbac import get_security_context
from api.db.session import get_db_session
from api.providers.anthropic_provider import AnthropicProvider
from api.providers.base import BaseLLMProvider
from api.providers.openai_provider import OpenAIProvider
from api.repositories import (
    ExplanationRepository,
    QuizAttemptRepository,
    QuizRepository,
    SessionRepository,
    TopicRepository,
)
from api.services.ai.explanation_generator import ExplanationGenerator
from api.services.ai.quiz_generator import QuizGenerator
from api.services.ai.insight_generator import InsightGenerator
from api.services.ai.mentor_tip_generator import MentorTipGenerator
from api.services.ai.recommendation_generator import RecommendationGenerator
from api.services.ai.summary_generator import SummaryGenerator
from api.services.ai_service import AIService
from api.services.insight_service import InsightService
from api.services.library_service import LibraryService
from api.services.cache.ai_cache_service import AICacheService
from api.services.health_service import HealthService
from api.services.prompt_service import PromptService
from api.services.response_parser import ResponseParser
from api.services.quiz_service import QuizService
from api.services.progress_service import ProgressService
from api.services.session_service import SessionService


# ---------------------------------------------------------------------------
# Stateless singletons (no DB state, safe to cache)
# ---------------------------------------------------------------------------

@lru_cache
def get_prompt_service() -> PromptService:
    return PromptService(Path(__file__).resolve().parent.parent / "prompts")


@lru_cache
def get_response_parser() -> ResponseParser:
    return ResponseParser()


from api.services.ai.groq_service import GroqService

def get_llm_provider(settings: Settings) -> BaseLLMProvider:
    if settings.llm_provider == "anthropic":
        return AnthropicProvider(
            api_key=settings.anthropic_api_key,
            timeout_seconds=settings.llm_timeout_seconds,
        )
    if settings.llm_provider == "groq":
        return GroqService(
            api_key=settings.groq_api_key,
            timeout_seconds=settings.llm_timeout_seconds,
        )
    return OpenAIProvider(
        api_key=settings.openai_api_key,
        timeout_seconds=settings.llm_timeout_seconds,
    )


def get_explanation_generator() -> ExplanationGenerator:
    settings = get_settings()
    prompt_service = get_prompt_service()
    return ExplanationGenerator(
        prompt_service=prompt_service,
        provider=get_llm_provider(settings),
        response_parser=get_response_parser(),
        system_prompt=prompt_service.get_system_prompt(),
        model=settings.llm_model_primary,
    )


def get_summary_generator() -> SummaryGenerator:
    settings = get_settings()
    prompt_service = get_prompt_service()
    return SummaryGenerator(
        prompt_service=prompt_service,
        provider=get_llm_provider(settings),
        response_parser=get_response_parser(),
        system_prompt=prompt_service.get_system_prompt(),
        model=settings.llm_model_primary,
    )


def get_quiz_generator() -> QuizGenerator:
    settings = get_settings()
    prompt_service = get_prompt_service()
    return QuizGenerator(
        prompt_service=prompt_service,
        provider=get_llm_provider(settings),
        response_parser=get_response_parser(),
        system_prompt=prompt_service.get_system_prompt(),
        model=settings.llm_model_primary,
    )


def get_insight_generator() -> InsightGenerator:
    settings = get_settings()
    prompt_service = get_prompt_service()
    return InsightGenerator(
        prompt_service=prompt_service,
        provider=get_llm_provider(settings),
        response_parser=get_response_parser(),
        system_prompt=prompt_service.get_system_prompt(),
        model=settings.llm_model_primary,
    )


def get_mentor_tip_generator() -> MentorTipGenerator:
    settings = get_settings()
    prompt_service = get_prompt_service()
    return MentorTipGenerator(
        prompt_service=prompt_service,
        provider=get_llm_provider(settings),
        response_parser=get_response_parser(),
        system_prompt=prompt_service.get_system_prompt(),
        model=settings.llm_model_primary,
    )


def get_recommendation_generator() -> RecommendationGenerator:
    settings = get_settings()
    prompt_service = get_prompt_service()
    return RecommendationGenerator(
        prompt_service=prompt_service,
        provider=get_llm_provider(settings),
        response_parser=get_response_parser(),
        system_prompt=prompt_service.get_system_prompt(),
        model=settings.llm_model_primary,
    )


def get_insight_service(
    db: AsyncSession = Depends(get_db_session),
) -> InsightService:
    return InsightService(
        topic_repo=TopicRepository(db),
        attempt_repo=QuizAttemptRepository(db),
        mentor_tip_generator=get_mentor_tip_generator(),
    )


def get_library_service(
    db: AsyncSession = Depends(get_db_session),
) -> LibraryService:
    return LibraryService(
        topic_repo=TopicRepository(db),
        explanation_repo=ExplanationRepository(db),
    )





def get_ai_cache_service() -> AICacheService:
    return AICacheService()


# ---------------------------------------------------------------------------
# Per-request dependencies (DB-backed, NOT cached)
# ---------------------------------------------------------------------------

def get_active_security_context(request: Request):
    return get_security_context(request)


def get_session_service(
    db: AsyncSession = Depends(get_db_session),
) -> SessionService:
    return SessionService(session_repo=SessionRepository(db))


def get_quiz_service(
    db: AsyncSession = Depends(get_db_session),
) -> QuizService:
    return QuizService(
        quiz_repo=QuizRepository(db),
        attempt_repo=QuizAttemptRepository(db),
        topic_repo=TopicRepository(db),
        progress_service=get_progress_service(db),
        insight_service=get_insight_service(db),
    )


def get_ai_service(
    db: AsyncSession = Depends(get_db_session),
) -> AIService:
    return AIService(
        quiz_service=QuizService(
            quiz_repo=QuizRepository(db),
            attempt_repo=QuizAttemptRepository(db),
            topic_repo=TopicRepository(db),
            progress_service=get_progress_service(db),
            insight_service=get_insight_service(db),
        ),
        session_service=SessionService(session_repo=SessionRepository(db)),
        explanation_generator=get_explanation_generator(),
        summary_generator=get_summary_generator(),
        quiz_generator=get_quiz_generator(),
        topic_repo=TopicRepository(db),
        explanation_repo=ExplanationRepository(db),
        cache_service=get_ai_cache_service(),
    )


def get_progress_service(
    db: AsyncSession = Depends(get_db_session),
) -> ProgressService:
    return ProgressService(
        topic_repo=TopicRepository(db),
        explanation_repo=ExplanationRepository(db),
        quiz_repo=QuizRepository(db),
        attempt_repo=QuizAttemptRepository(db),
        recommendation_generator=get_recommendation_generator(),
    )


def get_health_service(
    db: AsyncSession = Depends(get_db_session),
) -> HealthService:
    return HealthService(db_session=db)
