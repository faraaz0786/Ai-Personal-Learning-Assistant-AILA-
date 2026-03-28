import pytest

from core.config import Settings
from schemas.learn import ExplanationOutput, QuizGenerationOutput, SummaryOutput
from services.ai.explanation_generator import ExplanationGenerator
from services.ai.quiz_generator import QuizGenerator
from services.ai.summary_generator import SummaryGenerator
from services.prompt_service import PromptService
from services.response_parser import ResponseParser


class StubProvider:
    def __init__(self, responses: list[str]) -> None:
        self.responses = responses

    async def complete(self, **_: object) -> str:
        return self.responses.pop(0)


class StubPromptService(PromptService):
    def __init__(self) -> None:
        pass

    def render(self, template_name: str, **context: object) -> str:
        return f"{template_name}:{context}"

    def get_system_prompt(self) -> str:
        return "system"


@pytest.mark.asyncio
async def test_explanation_generator_returns_documented_schema() -> None:
    prompt_service = StubPromptService()
    settings = Settings()
    generator = ExplanationGenerator(
        prompt_service=prompt_service,
        provider=StubProvider(
            [
                (
                    '{"definition":"Photosynthesis is the process plants use to convert '
                    'light energy into stored chemical energy for growth and survival.",'
                    '"mechanism":"Plants absorb sunlight through chlorophyll and combine '
                    'water with carbon dioxide to create glucose and oxygen through '
                    'linked reactions in chloroplasts.",'
                    '"example":"A sunflower leaf uses sunlight, water, and carbon dioxide '
                    'to make glucose that supports the plant."}'
                )
            ]
        ),
        response_parser=ResponseParser(),
        system_prompt=prompt_service.get_system_prompt(),
        model=settings.llm_model_primary,
    )

    result = await generator.generate(topic="Photosynthesis", subject="Science")

    assert isinstance(result, ExplanationOutput)


@pytest.mark.asyncio
async def test_summary_generator_returns_documented_schema() -> None:
    prompt_service = StubPromptService()
    settings = Settings()
    generator = SummaryGenerator(
        prompt_service=prompt_service,
        provider=StubProvider(
            [
                (
                    '{"summary":"Photosynthesis lets plants capture sunlight and turn it '
                    'into stored chemical energy. It mainly happens in chloroplasts, '
                    'where water and carbon dioxide are converted into glucose and '
                    'oxygen. This process supports plant growth and contributes oxygen '
                    'to the atmosphere. It is one of the core biological systems that '
                    'supports food chains and life on Earth."}'
                )
            ]
        ),
        response_parser=ResponseParser(),
        system_prompt=prompt_service.get_system_prompt(),
        model=settings.llm_model_primary,
    )

    result = await generator.generate(
        topic="Photosynthesis",
        explanation="Definition: x\nMechanism: y\nExample: z",
    )

    assert isinstance(result, SummaryOutput)


@pytest.mark.asyncio
async def test_quiz_generator_returns_documented_schema() -> None:
    prompt_service = StubPromptService()
    settings = Settings()
    generator = QuizGenerator(
        prompt_service=prompt_service,
        provider=StubProvider(
            [
                (
                    '{"questions":[{"id":1,"question":"What is the main goal of '
                    'photosynthesis in plants?","options":["Make glucose","Produce '
                    'plastic","Create rocks","Form metal"],"correct_index":0,'
                    '"explanation":"Photosynthesis allows plants to make glucose from '
                    'sunlight, water, and carbon dioxide."}]}'
                )
            ]
        ),
        response_parser=ResponseParser(),
        system_prompt=prompt_service.get_system_prompt(),
        model=settings.llm_model_primary,
    )

    result = await generator.generate(
        topic="Photosynthesis",
        count=1,
        difficulty="easy",
    )

    assert isinstance(result, QuizGenerationOutput)
