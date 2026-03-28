import httpx

from api.core.exceptions import AppError
from api.providers.base import BaseLLMProvider


class AnthropicProvider(BaseLLMProvider):
    def __init__(self, api_key: str | None, timeout_seconds: int) -> None:
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    async def complete(
        self,
        *,
        prompt: str,
        system: str,
        model: str,
        max_tokens: int,
        response_format: str | None = None,
    ) -> str:
        _ = response_format
        if not self.api_key:
            raise AppError(
                status_code=503,
                code="LLM_UNAVAILABLE",
                message="Anthropic provider is not configured.",
            )

        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": 0.3,
            "system": system,
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json=payload,
                )
        except httpx.TimeoutException as exc:
            raise AppError(
                status_code=504,
                code="LLM_TIMEOUT",
                message="The LLM provider timed out.",
            ) from exc
        except httpx.HTTPError as exc:
            raise AppError(
                status_code=503,
                code="LLM_UNAVAILABLE",
                message="Failed to reach the LLM provider.",
            ) from exc

        if response.status_code >= 400:
            raise AppError(
                status_code=503,
                code="LLM_UNAVAILABLE",
                message="The LLM provider returned an error.",
                details={"provider_status": response.status_code},
            )

        data = response.json()
        try:
            return "".join(
                item["text"] for item in data["content"] if item.get("type") == "text"
            )
        except (KeyError, TypeError) as exc:
            raise AppError(
                status_code=503,
                code="LLM_UNAVAILABLE",
                message="The LLM provider returned an invalid response.",
            ) from exc
