import httpx
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.core.exceptions import AppError
from app.providers.base import BaseLLMProvider

logger = logging.getLogger(__name__)

class GroqService(BaseLLMProvider):
    def __init__(self, api_key: str | None, timeout_seconds: int) -> None:
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    @retry(
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def complete(
        self,
        *,
        prompt: str,
        system: str,
        model: str,
        max_tokens: int,
        response_format: str | None = None,
    ) -> str:
        if not self.api_key:
            raise AppError(
                status_code=503,
                code="INVALID_API_KEY",
                message="Groq provider is not configured.",
            )

        payload: dict[str, object] = {
            "model": model,
            "temperature": 0.3,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        }
        if response_format:
            payload["response_format"] = {"type": response_format}

        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
        except httpx.TimeoutException as exc:
            logger.error(f"Groq API timeout after {self.timeout_seconds}s")
            raise AppError(
                status_code=503,
                code="AI_TIMEOUT",
                message="AI service is currently unavailable. Please try again shortly.",
                details={"provider_status": "groq_failed_timeout"}
            ) from exc
        except httpx.HTTPError as exc:
            logger.error(f"Groq API HTTP error: {exc}")
            raise AppError(
                status_code=503,
                code="AI_PROVIDER_ERROR",
                message="AI service is currently unavailable. Please try again shortly.",
                details={"provider_status": "groq_failed_http"}
            ) from exc

        if response.status_code >= 400:
            logger.error(f"Groq API returned error {response.status_code}: {response.text}")
            error_code = "AI_PROVIDER_ERROR"
            
            if response.status_code in (401, 403):
                error_code = "INVALID_API_KEY"
            elif response.status_code == 400:
                error_code = "INVALID_MODEL"
                
            raise AppError(
                status_code=503,
                code=error_code,
                message="AI service is currently unavailable. Please try again shortly.",
                details={"provider_status": f"groq_failed_{response.status_code}"},
            )

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            logger.error(f"Groq API returned invalid JSON structure: {data}")
            raise AppError(
                status_code=503,
                code="AI_PROVIDER_ERROR",
                message="AI service is currently unavailable. Please try again shortly.",
                details={"provider_status": "groq_failed_parsing"}
            ) from exc
