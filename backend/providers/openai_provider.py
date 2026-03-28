import httpx

from core.exceptions import AppError
from providers.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
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
        if not self.api_key:
            raise AppError(
                status_code=503,
                code="LLM_UNAVAILABLE",
                message="OpenAI provider is not configured.",
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
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
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
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise AppError(
                status_code=503,
                code="LLM_UNAVAILABLE",
                message="The LLM provider returned an invalid response.",
            ) from exc
