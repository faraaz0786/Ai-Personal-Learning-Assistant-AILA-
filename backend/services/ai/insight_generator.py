from schemas.insight import QuizInsightSchema
from services.ai.base_generator import BaseGenerator


class InsightGenerator(BaseGenerator[QuizInsightSchema]):
    async def generate(
        self,
        *,
        topic: str,
        score: int,
        total: int,
        accuracy: float,
    ) -> QuizInsightSchema:
        prompt = self.prompt_service.render(
            "insight_v1.j2",
            topic=topic,
            score=score,
            total=total,
            accuracy=accuracy,
        )
        return await self.complete_json(
            task_name="insight",
            prompt=prompt,
            schema=QuizInsightSchema,
            max_tokens=500,
            response_format="json_object",
        )
