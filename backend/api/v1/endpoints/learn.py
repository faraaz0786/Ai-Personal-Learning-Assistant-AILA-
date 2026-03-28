import logging
from fastapi import APIRouter, Depends, Request

from core.dependencies import get_ai_service, get_session_service
from core.rbac import require_roles
from core.security import Role
from schemas.learn import (
    ExplainRequest,
    ExplainResponse,
    QuizRequest,
    QuizResponse,
    TopicResponse,
)
from services.ai_service import AIService
from services.session_service import SessionService


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/explain", response_model=ExplainResponse)
async def explain_topic(
    request: Request,
    payload: ExplainRequest,
    ai_service: AIService = Depends(get_ai_service),
) -> ExplainResponse:
    session_id = request.state.session_id
    logger.debug("Received explain request for topic: %s (session: %s)", payload.topic, session_id)
    response = await ai_service.explain(payload, session_id)
    logger.debug("Explain response generated: %s", response.topic_id)
    return response


@router.post("/quiz", response_model=QuizResponse)
async def generate_quiz(
    request: Request,
    payload: QuizRequest,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    ai_service: AIService = Depends(get_ai_service),
) -> QuizResponse:
    session_id = request.state.session_id
    logger.debug("Received quiz request for topic: %s (session: %s)", payload.topic_id, session_id)
    response = await ai_service.generate_quiz(payload, session_id)
    logger.debug("Quiz response generated: %s", response.quiz_id)
    return response





@router.get("/topics", response_model=list[TopicResponse])
async def list_topics(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    ai_service: AIService = Depends(get_ai_service),
) -> list[TopicResponse]:
    session_id = request.state.session_id
    return await ai_service.list_topics(session_id, limit=limit, offset=offset)


@router.get("/topics/{topic_id}", response_model=ExplainResponse)
async def get_topic(
    topic_id: str,
    request: Request,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    ai_service: AIService = Depends(get_ai_service),
) -> ExplainResponse:
    session_id = request.state.session_id
    return await ai_service.get_topic(topic_id, session_id)
