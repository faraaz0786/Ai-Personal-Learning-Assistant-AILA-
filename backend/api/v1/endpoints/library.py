from fastapi import APIRouter, Depends, Request
from app.core.dependencies import get_library_service, get_session_service
from app.core.rbac import require_roles
from app.core.security import Role
from app.schemas.library import LibraryResponse
from app.services.library_service import LibraryService
from app.services.session_service import SessionService

router = APIRouter()

@router.get("", response_model=LibraryResponse)
async def get_library(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    library_service: LibraryService = Depends(get_library_service),
    session_service: SessionService = Depends(get_session_service),
) -> LibraryResponse:
    session_id = await session_service.require_session(request.state.session_id)
    return await library_service.get_library(str(session_id), limit=limit, offset=offset)
