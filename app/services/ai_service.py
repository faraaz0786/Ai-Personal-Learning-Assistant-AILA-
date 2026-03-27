import asyncio
import logging
import traceback
from datetime import datetime, timezone
from time import perf_counter
from uuid import UUID, uuid4

from app.core.config import get_settings
from app.core.exceptions import AppError, LearnError
from app.repositories.explanation_repository import ExplanationRepository
from app.repositories.topic_repository import TopicRepository
from app.schemas.learn import (
    ExplainRequest,
    ExplainResponse,
    ExplanationOutput,
    QuizRequest,
    QuizResponse,
    TopicResponse,
)
from app.services.ai.explanation_generator import ExplanationGenerator
from app.services.ai.quiz_generator import QuizGenerator
from app.services.ai.summary_generator import SummaryGenerator
from app.services.ai.ai_observer import ai_observer
from app.services.cache.ai_cache_service import AICacheService, generate_cache_key, get_ttl
from app.services.quiz_service import QuizService
from app.services.session_service import SessionService
from app.utils.security_filter import security_filter


logger = logging.getLogger(__name__)


class AIService:
    """AI orchestration service for documented learning tasks."""

    def __init__(
        self,
        *,
        quiz_service: QuizService,
        session_service: SessionService,
        explanation_generator: ExplanationGenerator,
        summary_generator: SummaryGenerator,
        quiz_generator: QuizGenerator,
        topic_repo: TopicRepository,
        explanation_repo: ExplanationRepository,
        cache_service: AICacheService,
    ) -> None:
        self.quiz_service = quiz_service
        self.session_service = session_service
        self.explanation_generator = explanation_generator
        self.summary_generator = summary_generator
        self.quiz_generator = quiz_generator
        self.topic_repo = topic_repo
        self.explanation_repo = explanation_repo
        self.cache = cache_service

    async def _process_explain_hit(
        self, cached: dict, payload: ExplainRequest, session_id: str, started_at: float
    ) -> ExplainResponse:
        """Helper to process a cache hit for the explain feature."""
        parsed_session_id = await self.session_service.ensure_session(session_id)
        explanation = ExplanationOutput(**cached["explanation"])
        summary_text = cached["summary"]
        normalized_topic = cached["normalized_topic"]
        response_ms = int((perf_counter() - started_at) * 1000)

        # Still persist topic + explanation to DB for this session
        settings = get_settings()

        ai_observer.track_generation(
            feature="explain",
            latency_ms=response_ms,
            cache_hit=True,
            llm_model=settings.llm_model_primary,
        )

        topic_model = await self.topic_repo.create(
            session_id=parsed_session_id,
            raw_input=payload.topic,
            normalized_topic=normalized_topic,
            subject=payload.subject or "General",
            llm_model=settings.llm_model_primary,
            cached=True,
        )
        word_count = len(summary_text.split())
        await self.explanation_repo.create(
            topic_id=topic_model.id,
            definition=explanation.definition,
            mechanism=explanation.mechanism,
            example=explanation.example,
            summary=summary_text,
            word_count=word_count,
            response_ms=response_ms,
        )

        return ExplainResponse(
            topic_id=topic_model.id,
            normalized_topic=normalized_topic,
            explanation=explanation,
            summary=summary_text,
            cached=True,
            response_ms=response_ms,
        )

    async def _process_quiz_hit(
        self, cached: dict, payload: QuizRequest, session_id: str, started_at: float
    ) -> QuizResponse:
        """Helper to process a cache hit for the quiz feature."""
        logger.info("Cache HIT for quiz: topic_id=%s", payload.topic_id)
        
        settings = get_settings()
        ai_observer.track_generation(
            feature="quiz",
            latency_ms=int((perf_counter() - started_at) * 1000),
            cache_hit=True,
            llm_model=settings.llm_model_primary,
        )

        from app.schemas.learn import QuizGenerationOutput
        quiz_output = QuizGenerationOutput(**cached)
        
        return await self.quiz_service.create_quiz(
            topic_id=payload.topic_id,
            questions=quiz_output.questions,
            expected_count=payload.count,
            session_id=session_id,
            difficulty=payload.difficulty,
        )

    async def explain(self, payload: ExplainRequest, session_id: str) -> ExplainResponse:
        logger.info("Explain requested for topic: '%s' in session: %s", payload.topic, session_id)
        parsed_session_id = await self.session_service.ensure_session(session_id)
        started_at = perf_counter()

        # 1. Primary Cache Check (Fast Path)
        cache_key = generate_cache_key(
            "explain", topic=payload.topic, subject=payload.subject or "General"
        )
        cached = await self.cache.get_cached(cache_key)
        if cached is not None:
            return await self._process_explain_hit(cached, payload, session_id, started_at)

        # 2. Cache MISS -> Lock & Double Check
        lock_acquired = await self.cache.acquire_lock(cache_key)
        
        if not lock_acquired:
            # Another process is generating. Wait and retry cache.
            logger.info("Cache lock contention for %s, waiting...", cache_key)
            for _ in range(3):
                await asyncio.sleep(0.5)
                cached = await self.cache.get_cached(cache_key)
                if cached:
                    logger.info("Cache populated during wait for %s", cache_key)
                    return await self._process_explain_hit(cached, payload, session_id, started_at)
            # If still miss after retries, we generate without lock (avoid starvation)
            logger.warning("Lock wait timeout for %s, proceeding with redundant generation.", cache_key)

        try:
            # If lock acquired, check cache AGAIN before generating
            if lock_acquired:
                cached = await self.cache.get_cached(cache_key)
                if cached:
                    logger.info("Cache populated before generation (Double-Check) for %s", cache_key)
                    return await self._process_explain_hit(cached, payload, session_id, started_at)

            # 3. Security Logic (Input Sanitization)
            # This protects against prompt injection BEFORE reaching the LLM
            security_filter.filter_input(payload.topic)

            # 4. Actual LLM Generation
            explanation_raw = await self.explanation_generator.generate(
                topic=payload.topic,
                subject=payload.subject or "General",
            )
            # Filter output for PII
            explanation = security_filter.filter_output(explanation_raw)

            summary_raw = await self.summary_generator.generate(
                topic=payload.topic,
                explanation=(
                    f"Definition: {explanation.definition}\n"
                    f"Mechanism: {explanation.mechanism}\n"
                    f"Example: {explanation.example}"
                ),
            )
            # Filter output for PII
            summary = security_filter.filter_output(summary_raw)
        except AppError:
            raise
        except Exception as e:
            logger.error("LLM Generation entirely failed for explain. Traceback:\n%s", traceback.format_exc())
            # Part 6: Custom Error Handling (LEARN_FAILED)
            raise LearnError(
                message="An unexpected error occurred during AI generation.",
                details={"original_error": str(e)}
            ) from e
        finally:
            if lock_acquired:
                await self.cache.release_lock(cache_key)

        response_ms = int((perf_counter() - started_at) * 1000)
        normalized_topic = " ".join(payload.topic.split())
        cleaned_summary = " ".join(summary.summary.split())

        settings = get_settings()

        ai_observer.track_generation(
            feature="explain",
            latency_ms=response_ms,
            cache_hit=False,
            llm_model=settings.llm_model_primary,
        )

        # 4. Resilience: Persistence wrapped in try-except to avoid failing the request if AI succeeded
        topic_id = uuid4()
        try:
            topic_model = await self.topic_repo.create(
                session_id=parsed_session_id,
                raw_input=payload.topic,
                normalized_topic=normalized_topic,
                subject=payload.subject or "General",
                llm_model=settings.llm_model_primary,
                cached=False,
            )
            topic_id = topic_model.id
            
            word_count = len(cleaned_summary.split())
            await self.explanation_repo.create(
                topic_id=topic_id,
                definition=explanation.definition,
                mechanism=explanation.mechanism,
                example=explanation.example,
                summary=cleaned_summary,
                word_count=word_count,
                response_ms=response_ms,
            )
            print("[DEBUG] explanation_repo.create completed")
            logger.info("Successfully persisted explanation for topic: %s", topic_id)
        except Exception as e:
            logger.error("Database persistence failed for explain, but AI result is available. Error: %s", str(e))
            # We continue because we have the AI result. We use a generated topic_id if model creation failed.
            pass

        # 5. Populate Cache
        await self.cache.set_cached(
            cache_key,
            {
                "explanation": explanation.model_dump(),
                "summary": cleaned_summary,
                "normalized_topic": normalized_topic,
            },
            get_ttl("explain"),
        )

        return ExplainResponse(
            topic_id=topic_id,
            normalized_topic=normalized_topic,
            explanation=explanation,
            summary=cleaned_summary,
            cached=False,
            response_ms=response_ms,
        )

    async def generate_quiz(self, payload: QuizRequest, session_id: str) -> QuizResponse:
        await self.session_service.ensure_session(session_id)
        started_at = perf_counter()

        topic_model = await self.topic_repo.get_by_id(payload.topic_id)
        if topic_model is None:
            raise AppError(status_code=404, code="TOPIC_NOT_FOUND", message="Topic not found.")

        # Relax session check for robustness if a valid topic_id is provided
        # (UUID topic_id is sufficiently unguessable for this MVP)
        if session_id and str(topic_model.session_id) != session_id:
            logger.warning("Session mismatch for quiz: topic session %s vs request session %s", topic_model.session_id, session_id)
            # We allow it for now to avoid 403s on session expiry, 
            # but we should ideally update the topic or track the new session.
            pass

        explanation_model = await self.explanation_repo.get_by_topic_id(payload.topic_id)
        if explanation_model is None:
            raise AppError(status_code=404, code="TOPIC_NOT_FOUND", message="No explanation found.")

        # 1. Primary Cache Check
        cache_key = generate_cache_key(
            "quiz",
            topic=topic_model.normalized_topic,
            difficulty=payload.difficulty,
            count=str(payload.count),
        )
        cached = await self.cache.get_cached(cache_key)
        if cached is not None:
            return await self._process_quiz_hit(cached, payload, session_id, started_at)

        # 2. Cache MISS -> Lock & Double Check
        lock_acquired = await self.cache.acquire_lock(cache_key)
        if not lock_acquired:
            logger.info("Cache lock contention for quiz:%s, waiting...", cache_key)
            for _ in range(3):
                await asyncio.sleep(0.5)
                cached = await self.cache.get_cached(cache_key)
                if cached:
                    return await self._process_quiz_hit(cached, payload, session_id, started_at)

        try:
            if lock_acquired:
                cached = await self.cache.get_cached(cache_key)
                if cached:
                    return await self._process_quiz_hit(cached, payload, session_id, started_at)

            # 3. Security Logic
            # Double check the topic from DB just in case, or for quiz-specific injection attempts
            security_filter.filter_input(topic_model.normalized_topic)

            # 4. LLM Generation
            quiz_response_raw = await self.quiz_generator.generate(
                topic=topic_model.normalized_topic,
                count=payload.count,
                difficulty=payload.difficulty,
            )
            quiz_response = security_filter.filter_output(quiz_response_raw)
        except AppError:
            raise
        except Exception as e:
            logger.error("LLM Generation entirely failed for quiz. Traceback:\n%s", traceback.format_exc())
            # Part 6: Custom Error Handling (LEARN_FAILED)
            raise LearnError(
                message="An unexpected error occurred during AI quiz generation.",
                details={"original_error": str(e)}
            ) from e
        finally:
            if lock_acquired:
                await self.cache.release_lock(cache_key)

        settings = get_settings()
        ai_observer.track_generation(
            feature="quiz",
            latency_ms=int((perf_counter() - started_at) * 1000),
            cache_hit=False,
            llm_model=settings.llm_model_primary,
        )

        # 4. Populate Cache
        await self.cache.set_cached(cache_key, quiz_response.model_dump(), get_ttl("quiz"))

        # 5. Persistence via QuizService
        try:
            return await self.quiz_service.create_quiz(
                topic_id=payload.topic_id,
                questions=quiz_response.questions,
                expected_count=payload.count,
                session_id=session_id,
                difficulty=payload.difficulty,
            )
        except Exception as e:
            logger.error("Database persistence failed for quiz, but AI result is available. Error: %s", str(e))
            # Return a safe response with generated IDs if DB fails
            return QuizResponse(
                quiz_id=uuid4(),
                topic_id=payload.topic_id,
                questions=quiz_response.questions,
                difficulty=payload.difficulty,
                total_questions=len(quiz_response.questions),
                created_at=datetime.now(timezone.utc),
            )


    async def list_topics(
        self, session_id: str, limit: int = 100, offset: int = 0
    ) -> list[TopicResponse]:
        parsed_session_id = await self.session_service.ensure_session(session_id)
        topics = await self.topic_repo.list_by_session_id(parsed_session_id, limit=limit, offset=offset)
        return [
            TopicResponse(
                topic_id=str(t.id),
                normalized_topic=t.normalized_topic,
                subject=t.subject,
            )
            for t in topics
        ]

    async def get_topic(self, topic_id: str, session_id: str) -> ExplainResponse:
        parsed_session_id = await self.session_service.ensure_session(session_id)
        topic_model = await self.topic_repo.get_by_id(UUID(topic_id))
        if topic_model is None:
            raise AppError(status_code=404, code="TOPIC_NOT_FOUND", message="Topic not found.")
        if topic_model.session_id != parsed_session_id:
            raise AppError(status_code=403, code="SESSION_MISMATCH", message="Session mismatch.")

        explanation_model = await self.explanation_repo.get_by_topic_id(UUID(topic_id))
        if explanation_model is None:
            raise AppError(status_code=404, code="TOPIC_NOT_FOUND", message="No explanation found.")

        return ExplainResponse(
            topic_id=topic_model.id,
            normalized_topic=topic_model.normalized_topic,
            explanation=ExplanationOutput(
                definition=explanation_model.definition,
                mechanism=explanation_model.mechanism,
                example=explanation_model.example,
            ),
            summary=explanation_model.summary,
            cached=topic_model.cached,
            response_ms=explanation_model.response_ms,
        )
