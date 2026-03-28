from fastapi import APIRouter, Depends, Request

from core.dependencies import get_progress_service, get_session_service
from core.rbac import require_roles
from core.security import Role
from schemas.progress import DashboardSummary, ProgressHistoryItem, ProgressRecommendation, ProgressSummary
from services.progress_service import ProgressService
from services.session_service import SessionService


router = APIRouter()


@router.get("/summary", response_model=ProgressSummary)
async def get_progress_summary(
    request: Request,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    progress_service: ProgressService = Depends(get_progress_service),
    session_service: SessionService = Depends(get_session_service),
) -> ProgressSummary:
    session_id = await session_service.require_session(request.state.session_id)
    return await progress_service.summarize_progress(str(session_id))


@router.get("/dashboard", response_model=DashboardSummary)
async def get_dashboard_summary(
    request: Request,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    progress_service: ProgressService = Depends(get_progress_service),
    session_service: SessionService = Depends(get_session_service),
) -> DashboardSummary:
    session_id = await session_service.require_session(request.state.session_id)
    return await progress_service.get_dashboard_summary(str(session_id))


@router.get("/history", response_model=list[ProgressHistoryItem])
async def get_progress_history(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    progress_service: ProgressService = Depends(get_progress_service),
    session_service: SessionService = Depends(get_session_service),
) -> list[ProgressHistoryItem]:
    session_id = await session_service.require_session(request.state.session_id)
    return await progress_service.get_history(str(session_id), limit=limit, offset=offset)


@router.get("/recommendations", response_model=list[ProgressRecommendation])
async def get_recommendations(
    request: Request,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    progress_service: ProgressService = Depends(get_progress_service),
    session_service: SessionService = Depends(get_session_service),
) -> list[ProgressRecommendation]:
    session_id = await session_service.require_session(request.state.session_id)
    return await progress_service.get_recommendations(str(session_id))
