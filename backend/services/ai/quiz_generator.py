from api.schemas.learn import QuizGenerationOutput
from api.services.ai.base_generator import BaseGenerator


class QuizGenerator(BaseGenerator[QuizGenerationOutput]):
    async def generate(
        self,
        *,
        topic: str,
        difficulty: str,
        count: int,
    ) -> QuizGenerationOutput:
        prompt = self.prompt_service.render(
            "quiz_v1.j2",
            topic=topic,
            count=count,
            difficulty=difficulty,
        )
        return await self.complete_json(
            task_name="quiz",
            prompt=prompt,
            schema=QuizGenerationOutput,
            max_tokens=800,
            response_format="json_object",
        )
