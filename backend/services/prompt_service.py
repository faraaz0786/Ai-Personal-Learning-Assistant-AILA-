from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


class PromptService:
    def __init__(self, prompt_directory: Path) -> None:
        self.prompt_directory = prompt_directory
        self.environment = Environment(
            loader=FileSystemLoader(str(prompt_directory)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=StrictUndefined,
        )

    def render(self, template_name: str, **context: object) -> str:
        template = self.environment.get_template(template_name)
        return template.render(**context)

    def get_system_prompt(self) -> str:
        """Load and return the system persona dynamically."""
        return (self.prompt_directory / "system_v1.txt").read_text(encoding="utf-8")
