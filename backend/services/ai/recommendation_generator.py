from api.schemas.progress import ProgressRecommendation
from api.services.ai.base_generator import BaseGenerator
from pydantic import BaseModel

class RecommendationOutput(BaseModel):
    recommendations: list[ProgressRecommendation]

class RecommendationGenerator(BaseGenerator[RecommendationOutput]):
    async def generate(
        self,
        *,
        topics: list[str],
        performance_summary: str,
    ) -> RecommendationOutput:
        prompt = self.prompt_service.render(
            "recommend_v1.j2",
            topics=topics,
            performance_summary=performance_summary,
        )
        return await self.complete_json(
            task_name="recommendation",
            prompt=prompt,
            schema=RecommendationOutput,
            max_tokens=600,
            response_format="json_object",
        )
