import asyncio
import httpx
from typing import Generic, TypeVar

from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from core.circuit_breaker import ai_circuit_breaker, CircuitBreakerOpenException
from core.config import get_settings
from core.timing import timing_tracker
from providers.base import BaseLLMProvider
from services.prompt_service import PromptService
from services.response_parser import ResponseParser
from core.exceptions import AppError


SchemaT = TypeVar("SchemaT", bound=BaseModel)


class BaseGenerator(Generic[SchemaT]):
    def __init__(
        self,
        *,
        prompt_service: PromptService,
        provider: BaseLLMProvider,
        response_parser: ResponseParser,
        system_prompt: str,
        model: str,
    ) -> None:
        self.prompt_service = prompt_service
        self.provider = provider
        self.response_parser = response_parser
        self.system_prompt = system_prompt
        self.model = model

    @retry(
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError, asyncio.TimeoutError)),
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def _invoke_llm_with_retry(
        self, prompt_to_send: str, max_tokens: int, response_format: str | None
    ) -> str:
        """Internal helper orchestrating strict retry, circuit breaking, and hard timeouts."""
        ai_circuit_breaker.check()
        settings = get_settings()
        
        try:
            with timing_tracker.measure("ai"):
                raw_content = await asyncio.wait_for(
                    self.provider.complete(
                        prompt=prompt_to_send,
                        system=self.system_prompt,
                        model=self.model,
                        max_tokens=max_tokens,
                        response_format=response_format,
                    ),
                    timeout=settings.llm_timeout_seconds,
                )
            ai_circuit_breaker.record_success()
            return raw_content
        except (asyncio.TimeoutError, AppError, CircuitBreakerOpenException) as e:
            ai_circuit_breaker.record_failure()
            if isinstance(e, asyncio.TimeoutError):
                raise AppError(
                    status_code=503,
                    code="AI_TIMEOUT",
                    message="AI service is currently unavailable. Please try again shortly.",
                    details={"provider_status": "ai_failed_timeout"}
                ) from e
            if isinstance(e, CircuitBreakerOpenException):
                raise AppError(
                    status_code=503,
                    code="AI_CIRCUIT_OPEN",
                    message="AI service is temporarily suspended due to multiple failures.",
                    details={"provider_status": "circuit_open"}
                ) from e
            raise e
        except Exception as e:
            ai_circuit_breaker.record_failure()
            raise e

    async def complete_json(
        self,
        *,
        task_name: str,
        prompt: str,
        schema: type[SchemaT],
        max_tokens: int,
        response_format: str | None = None,
    ) -> SchemaT:
        last_error = None

        for attempt in range(2):
            prompt_to_send = prompt
            if attempt == 1:
                prompt_to_send = (
                    f"{prompt}\n\n"
                    "Your previous response was not valid JSON. "
                    "Please respond ONLY with the JSON object, no other text."
                )

            try:
                raw_content = await self._invoke_llm_with_retry(
                    prompt_to_send, max_tokens, response_format
                )

                return self.response_parser.parse(
                    raw_content=raw_content,
                    schema=schema,
                    task_name=task_name,
                )
            except Exception as exc:  # parser already normalizes expected app errors
                last_error = exc

        raise last_error  # type: ignore[misc]
