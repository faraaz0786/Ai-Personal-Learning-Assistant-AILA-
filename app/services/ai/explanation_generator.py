from app.schemas.learn import ExplanationOutput
from app.services.ai.base_generator import BaseGenerator


class ExplanationGenerator(BaseGenerator[ExplanationOutput]):
    async def generate(self, *, topic: str, subject: str) -> ExplanationOutput:
        prompt = self.prompt_service.render("explain_v1.j2", topic=topic, subject=subject)
        return await self.complete_json(
            task_name="explain",
            prompt=prompt,
            schema=ExplanationOutput,
            max_tokens=1000,
        )
