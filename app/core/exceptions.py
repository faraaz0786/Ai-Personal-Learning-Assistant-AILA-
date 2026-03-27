class AppError(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        details: dict | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or {}
class LearnError(AppError):
    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(
            status_code=500,
            code="LEARN_FAILED",
            message=message,
            details={"fallback": True, **(details or {})}
        )
