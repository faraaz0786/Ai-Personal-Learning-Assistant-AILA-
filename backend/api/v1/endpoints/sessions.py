from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status

from core.dependencies import get_session_service
from core.rbac import require_roles
from core.security import Role
from schemas.session import SessionResponse
from services.session_service import SessionService


router = APIRouter()


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    response: Response,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    session_service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    session = await session_service.generate_new_session()
    response.set_cookie(
        key="aila_session",
        value=str(session.session_id),
        httponly=True,
        samesite="none",
        secure=True,
    )
    return session


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: UUID,
    request: Request,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    session_service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    await session_service.assert_session_access(
        cookie_session_id=request.state.session_id,
        resource_session_id=session_id,
    )
    return await session_service.get_session(session_id)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: UUID,
    request: Request,
    response: Response,
    _: object = Depends(require_roles(Role.ANONYMOUS)),
    session_service: SessionService = Depends(get_session_service),
) -> None:
    await session_service.assert_session_access(
        cookie_session_id=request.state.session_id,
        resource_session_id=session_id,
    )
    await session_service.delete_session(session_id)
    response.delete_cookie("aila_session")
    return None
