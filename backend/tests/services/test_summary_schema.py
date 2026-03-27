import pytest
from pydantic import ValidationError

from app.schemas.learn import SummaryOutput


def test_summary_output_accepts_documented_word_range() -> None:
    summary = (
        "Photosynthesis allows plants to convert sunlight into stored chemical energy. "
        "It mainly occurs in chloroplasts, where carbon dioxide and water are turned "
        "into glucose and oxygen through linked reactions. This process fuels plant "
        "growth, supports food chains, and contributes oxygen to the atmosphere. It is "
        "a core biology concept for understanding energy transfer in living systems."
    )

    result = SummaryOutput(summary=summary)

    assert 60 <= len(result.summary.split()) <= 100


def test_summary_output_rejects_short_revision_summary() -> None:
    with pytest.raises(ValidationError):
        SummaryOutput(summary="Photosynthesis is how plants make food from sunlight.")
