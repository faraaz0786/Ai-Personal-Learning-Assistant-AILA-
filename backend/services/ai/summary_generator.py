from api.schemas.learn import SummaryOutput
from api.services.ai.base_generator import BaseGenerator


class SummaryGenerator(BaseGenerator[SummaryOutput]):
    async def generate(self, *, topic: str, explanation: str) -> SummaryOutput:
        prompt = self.prompt_service.render(
            "summarize_v1.j2",
            topic=topic,
            explanation=explanation,
        )
        return await self.complete_json(
            task_name="summarize",
            prompt=prompt,
            schema=SummaryOutput,
            max_tokens=300,
        )
