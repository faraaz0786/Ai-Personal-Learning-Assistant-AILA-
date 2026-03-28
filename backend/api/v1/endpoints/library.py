from fastapi import APIRouter, Depends, Request
from api.core.dependencies import get_library_service, get_session_service
from api.core.rbac import require_roles
from api.core.security import Role
from api.schemas.library import LibraryResponse
from api.services.library_service import LibraryService
from api.services.session_service import SessionService

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
