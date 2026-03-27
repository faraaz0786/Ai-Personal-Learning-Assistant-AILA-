from app.services.prompt_service import PromptService


def test_explain_prompt_renders_correctly() -> None:
    service = PromptService()
    rendered = service.render("explain_v1.j2", topic="Black Holes", subject="Physics")
    assert "Black Holes" in rendered
    assert "Physics" in rendered
    assert "definition" in rendered.lower()


def test_quiz_prompt_renders_correctly() -> None:
    service = PromptService()
    rendered = service.render("quiz_v1.j2", topic="Photosynthesis", count=5, difficulty="hard")
    assert "Photosynthesis" in rendered
    assert "5" in rendered
    assert "hard" in rendered


def test_summary_prompt_renders_correctly() -> None:
    service = PromptService()
    rendered = service.render(
        "summarize_v1.j2",
        topic="TCP/IP",
        explanation="It is a suite of communication protocols used to interconnect network devices on the internet.",
    )
    assert "TCP/IP" in rendered
    assert "communication protocols" in rendered
    assert "summary" in rendered.lower()


def test_system_prompt_loads() -> None:
    service = PromptService()
    system_text = service.get_system_prompt()
    assert len(system_text) > 50
    assert "tutor" in system_text.lower() or "assistant" in system_text.lower()
