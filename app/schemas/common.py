from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints


class HealthResponse(BaseModel):
    status: str
    detail: str | None = None


class ErrorDetail(BaseModel):
    code: Annotated[str, StringConstraints(strip_whitespace=True, to_upper=True)]
    message: Annotated[str, StringConstraints(strip_whitespace=True)]
    details: dict = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorDetail
