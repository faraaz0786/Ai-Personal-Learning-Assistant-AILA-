import pytest

from core.exceptions import AppError
from schemas.learn import ExplanationOutput
from services.response_parser import ResponseParser


def test_response_parser_accepts_valid_json_schema() -> None:
    parser = ResponseParser()

    result = parser.parse(
        raw_content=(
            '{"definition":"Photosynthesis is the process plants use to convert '
            'light energy into chemical energy for growth and survival.",'
            '"mechanism":"Plants absorb sunlight through chlorophyll, take in carbon '
            'dioxide and water, and convert them into glucose and oxygen through '
            'linked reactions in chloroplasts.",'
            '"example":"A sunflower leaf uses sunlight, water, and carbon dioxide to '
            'produce glucose for the plant."}'
        ),
        schema=ExplanationOutput,
        task_name="explain",
    )

    assert result.definition


def test_response_parser_rejects_invalid_json() -> None:
    parser = ResponseParser()

    with pytest.raises(AppError) as exc:
        parser.parse(
            raw_content="not-json",
            schema=ExplanationOutput,
            task_name="explain",
        )

    assert exc.value.code == "LLM_UNAVAILABLE"


def test_response_parser_rejects_documented_error_payload() -> None:
    parser = ResponseParser()

    with pytest.raises(AppError) as exc:
        parser.parse(
            raw_content=(
                '{"error":"Topic not recognized as an educational subject. '
                'Please enter a specific academic topic."}'
            ),
            schema=ExplanationOutput,
            task_name="explain",
        )

    assert exc.value.code == "VALIDATION_ERROR"
