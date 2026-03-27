from functools import lru_cache
from pathlib import Path

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.rbac import get_security_context
from app.db.session import get_db_session
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.base import BaseLLMProvider
from app.providers.openai_provider import OpenAIProvider
from app.repositories import (
    ExplanationRepository,
    QuizAttemptRepository,
    QuizRepository,
    SessionRepository,
    TopicRepository,
)
from app.services.ai.explanation_generator import ExplanationGenerator
from app.services.ai.quiz_generator import QuizGenerator
from app.services.ai.insight_generator import InsightGenerator
from app.services.ai.mentor_tip_generator import MentorTipGenerator
from app.services.ai.recommendation_generator import RecommendationGenerator
from app.services.ai.summary_generator import SummaryGenerator
from app.services.ai_service import AIService
from app.services.insight_service import InsightService
from app.services.library_service import LibraryService
from app.services.cache.ai_cache_service import AICacheService
from app.services.health_service import HealthService
from app.services.prompt_service import PromptService
from app.services.response_parser import ResponseParser
from app.services.quiz_service import QuizService
from app.services.progress_service import ProgressService
from app.services.session_service import SessionService


# ---------------------------------------------------------------------------
# Stateless singletons (no DB state, safe to cache)
# ---------------------------------------------------------------------------

@lru_cache
def get_prompt_service() -> PromptService:
    return PromptService(Path(__file__).resolve().parent.parent / "prompts")


@lru_cache
def get_response_parser() -> ResponseParser:
    return ResponseParser()


from app.services.ai.groq_service import GroqService

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
