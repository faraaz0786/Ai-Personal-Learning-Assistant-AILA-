from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    async def complete(
        self,
        *,
        prompt: str,
        system: str,
        model: str,
        max_tokens: int,
        response_format: str | None = None,
    ) -> str:
        raise NotImplementedError
