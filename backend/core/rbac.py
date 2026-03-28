from fastapi import Depends, Request

from core.exceptions import AppError
from core.security import Role, SecurityContext


import logging

logger = logging.getLogger(__name__)


def get_security_context(request: Request) -> SecurityContext:
    context = getattr(request.state, "security_context", None)
    if context is None:
        return SecurityContext(session_id=getattr(request.state, "session_id", None))
    return context


def require_roles(*allowed_roles: Role):
    async def dependency(
        context: SecurityContext = Depends(get_security_context),
    ) -> SecurityContext:
        allowed_values = [r.value for r in allowed_roles]
        if context.role.value not in allowed_values:
            raise AppError(
                status_code=403,
                code="FORBIDDEN",
                message="You do not have permission to access this resource.",
                details={"required_roles": allowed_values},
            )
        return context

    return dependency
