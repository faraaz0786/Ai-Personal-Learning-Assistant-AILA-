from datetime import datetime, timezone
import logging
from uuid import UUID

from core.exceptions import AppError
from repositories.session_repository import SessionRepository
from schemas.session import SessionResponse


logger = logging.getLogger(__name__)


class SessionService:
    def __init__(self, *, session_repo: SessionRepository) -> None:
        self.session_repo = session_repo

    async def generate_new_session(self) -> SessionResponse:
        model = await self.session_repo.create()
        return SessionResponse(
            id=model.id,
            created_at=model.created_at,
            last_active_at=model.last_active_at,
        )

    async def get_session(self, session_id: UUID) -> SessionResponse:
        model = await self.session_repo.get_by_id(session_id)
        if model is None:
            raise AppError(
                status_code=404,
                code="SESSION_NOT_FOUND",
                message="The requested session could not be found.",
            )

        updated = await self.session_repo.update_last_active(session_id)
        return SessionResponse(
            id=updated.id,
            created_at=updated.created_at,
            last_active_at=updated.last_active_at,
        )

    async def delete_session(self, session_id: UUID) -> None:
        deleted = await self.session_repo.delete_by_id(session_id)
        if not deleted:
            raise AppError(
                status_code=404,
                code="SESSION_NOT_FOUND",
                message="The requested session could not be found.",
            )

    async def ensure_session(self, session_id: str | None) -> UUID:
        """Get the parsed session UUID or create a new one if missing/invalid."""
        if not session_id:
            logger.info("Session ID missing in request, creating a new temporary session.")
            new_session = await self.generate_new_session()
            return new_session.session_id

        try:
            parsed = UUID(session_id)
            # Verify it exists in DB
            await self.get_session(parsed)
            return parsed
        except (ValueError, AppError):
            logger.warning("Session ID invalid or expired (%s), creating a new temporary session.", session_id)
            new_session = await self.generate_new_session()
            return new_session.session_id

    async def require_session(self, session_id: str | None) -> UUID:
        if not session_id:
            raise AppError(
                status_code=403,
                code="SESSION_MISMATCH",
                message="DEBUG: 403 SOURCE DETECTED",
            )

        try:
            parsed = UUID(session_id)
        except ValueError as exc:
            raise AppError(
                status_code=403,
                code="SESSION_MISMATCH",
                message="The provided session cookie is invalid.",
            ) from exc

        await self.get_session(parsed)
        return parsed

    async def assert_session_access(
        self, *, cookie_session_id: str | None, resource_session_id: UUID
    ) -> UUID:
        active_session_id = await self.require_session(cookie_session_id)
        if active_session_id != resource_session_id:
            raise AppError(
                status_code=403,
                code="SESSION_MISMATCH",
                message="The requested resource belongs to a different session.",
            )
        return active_session_id
