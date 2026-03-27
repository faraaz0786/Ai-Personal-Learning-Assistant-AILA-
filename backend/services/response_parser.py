import json
import logging
import re
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from app.core.exceptions import AppError
from app.core.security import sanitize_ai_payload


logger = logging.getLogger(__name__)

SchemaT = TypeVar("SchemaT", bound=BaseModel)


class ResponseParser:
    def parse(
        self,
        *,
        raw_content: str,
        schema: type[SchemaT],
        task_name: str,
    ) -> SchemaT:
        logger.info("Raw AI response for %s: %s", task_name, raw_content)

        # Strip markdown code fences if present
        cleaned_content = raw_content.strip()
        if cleaned_content.startswith("```"):
            # Remove opening fence (e.g., ```json or ```)
            cleaned_content = re.sub(r"^```(?:json)?\s*", "", cleaned_content, flags=re.MULTILINE)
            # Remove closing fence
            cleaned_content = re.sub(r"\s*```$", "", cleaned_content, flags=re.MULTILINE)
        
        parsed: Any = None
        try:
            parsed = json.loads(cleaned_content)
        except json.JSONDecodeError as exc:
            logger.warning("JSON parsing failed, attempting heuristic recovery for %s", task_name)
            parsed = self._heuristic_parse(cleaned_content)
            if not parsed:
                logger.error("Heuristic parsing also failed for %s. Content: %s", task_name, cleaned_content)
                raise AppError(
                    status_code=503,
                    code="LLM_UNAVAILABLE",
                    message="The LLM response was not valid JSON.",
                    details={"task": task_name},
                ) from exc

        if isinstance(parsed, dict) and "error" in parsed:
            raise AppError(
                status_code=400,
                code="VALIDATION_ERROR",
                message=str(parsed["error"]),
                details={"task": task_name},
            )

        try:
            # Sanitize the payload for any remaining PII/HTML
            sanitized_payload = sanitize_ai_payload(parsed)
            return schema.model_validate(sanitized_payload)
        except (ValidationError, ValueError) as exc:
            logger.error("Schema validation failed for %s: %s", task_name, exc)
            raise AppError(
                status_code=503,
                code="LLM_UNAVAILABLE",
                message="The LLM response did not match the required schema.",
                details={"task": task_name, "error": str(exc)},
            ) from exc

    def _heuristic_parse(self, content: str) -> dict | None:
        """Attempt to extract key-value pairs from a non-JSON string."""
        data = {}
        # Try to find "key": "value" or "key": value
        pairs = re.findall(r'"(\w+)":\s*(?:"([^"]*)"|(\d+)|(\{.*?\})|(\[.*?\]))', content, re.DOTALL)
        for key, val_str, val_int, val_obj, val_arr in pairs:
            if val_str:
                data[key] = val_str
            elif val_int:
                data[key] = int(val_int)
            # We don't handle nested objects/arrays easily with regex, 
            # but usually the top-level keys are enough.
        
        return data if data else None
