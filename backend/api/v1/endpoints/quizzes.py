from uuid import UUID

from fastapi import APIRouter, Depends, Request

from api.core.dependencies import get_quiz_service, get_session_service
from api.core.rbac import require_roles
from api.core.security import Role
from api.schemas.quiz import QuizAttemptRequest, QuizAttemptResponse, QuizDetailResponse
from api.services.quiz_service import QuizService
from api.services.session_service import SessionService


router = APIRouter()


@router.get("/{quiz_id}", response_model=QuizDetailResponse)
async def get_quiz(
    quiz_id: UUID,
    request: Request,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    quiz_service: QuizService = Depends(get_quiz_service),
    session_service: SessionService = Depends(get_session_service),
) -> QuizDetailResponse:
    session_id = await session_service.require_session(request.state.session_id)
    return await quiz_service.get_quiz(quiz_id, str(session_id))


@router.post("/{quiz_id}/attempts", response_model=QuizAttemptResponse)
async def submit_quiz_attempt(
    quiz_id: UUID,
    request: Request,
    payload: QuizAttemptRequest,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    quiz_service: QuizService = Depends(get_quiz_service),
    session_service: SessionService = Depends(get_session_service),
) -> QuizAttemptResponse:
    session_id = await session_service.require_session(request.state.session_id)
    return await quiz_service.submit_attempt(quiz_id, payload.answers, str(session_id))


@router.get("/{quiz_id}/attempts", response_model=list[QuizAttemptResponse])
async def list_quiz_attempts(
    quiz_id: UUID,
    request: Request,
    limit: int = 100,
    offset: int = 0,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    quiz_service: QuizService = Depends(get_quiz_service),
    session_service: SessionService = Depends(get_session_service),
) -> list[QuizAttemptResponse]:
    session_id = await session_service.require_session(request.state.session_id)
    return await quiz_service.list_attempts(quiz_id, str(session_id), limit=limit, offset=offset)
