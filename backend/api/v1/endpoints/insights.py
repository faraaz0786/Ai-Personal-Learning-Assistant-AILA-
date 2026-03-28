from fastapi import APIRouter, Depends, Request
from api.core.dependencies import get_insight_service, get_session_service
from api.core.rbac import require_roles
from api.core.security import Role
from api.schemas.insight import MentorTipSchema
from api.services.insight_service import InsightService
from api.services.session_service import SessionService

router = APIRouter()

@router.get("/mentor-tip", response_model=MentorTipSchema)
async def get_mentor_tip(
    request: Request,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    insight_service: InsightService = Depends(get_insight_service),
    session_service: SessionService = Depends(get_session_service),
) -> MentorTipSchema:
    session_id = await session_service.require_session(request.state.session_id)
    return await insight_service.get_mentor_tip(str(session_id))
