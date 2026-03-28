from schemas.insight import MentorTipSchema
from services.ai.base_generator import BaseGenerator


class MentorTipGenerator(BaseGenerator[MentorTipSchema]):
    async def generate(
        self,
        *,
        topic: str,
        accuracy: float,
        recent_activity: str,
    ) -> MentorTipSchema:
        prompt = self.prompt_service.render(
            "mentor_tip_v1.j2",
            topic=topic,
            accuracy=accuracy,
            recent_activity=recent_activity,
        )
        return await self.complete_json(
            task_name="mentor_tip",
            prompt=prompt,
            schema=MentorTipSchema,
            max_tokens=500,
            response_format="json_object",
        )
