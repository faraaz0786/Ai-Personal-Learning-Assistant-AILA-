import traceback
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
        try:
            model = await self.session_repo.create()

            return SessionResponse(
                id=model.id,
                created_at=model.created_at,
                last_active_at=model.last_active_at,
            )

        except Exception as e:
            print("🔥 SESSION CREATE ERROR:", str(e))
            traceback.print_exc()
            raise

    async def get_session(self, session_id: UUID) -> SessionResponse:
        try:
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

        except AppError:
            raise

        except Exception as e:
            print("🔥 GET SESSION ERROR:", str(e))
            traceback.print_exc()
            raise

    async def delete_session(self, session_id: UUID) -> None:
        try:
            deleted = await self.session_repo.delete_by_id(session_id)

            if not deleted:
                raise AppError(
                    status_code=404,
                    code="SESSION_NOT_FOUND",
                    message="The requested session could not be found.",
                )

        except Exception as e:
            print("🔥 DELETE SESSION ERROR:", str(e))
            traceback.print_exc()
            raise

    async def require_session(self, session_id: str | None) -> UUID:
        if not session_id:
            print("⚠️ SESSION MISSING")
            raise AppError(
                status_code=403,
                code="SESSION_MISSING",
                message="Session cookie not found.",
            )

        try:
            parsed = UUID(session_id)
        except Exception:
            print("⚠️ INVALID SESSION FORMAT:", session_id)
            raise AppError(
                status_code=403,
                code="SESSION_INVALID",
                message="Invalid session ID format.",
            )

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
                message="Resource belongs to another session.",
            )

        return active_session_id
        