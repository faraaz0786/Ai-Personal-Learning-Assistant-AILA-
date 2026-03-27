import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


BLOCKED_PROMPT_PATTERNS = (
    r"ignore previous instructions",
    r"you are now",
    r"system:",
)

OUTPUT_BLOCKED_PATTERNS = (
    r"<script",
    r"javascript:",
    r"data:text/html",
)

PII_PATTERNS = (
    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
    r"\b(?:\d[\s-]*?){13,16}\b",  # Credit Card
)


class Role(StrEnum):
    ANONYMOUS = "anonymous"
    ADMIN = "admin"


@dataclass(slots=True)
class SecurityContext:
    session_id: str | None
    role: Role = Role.ANONYMOUS


def strip_html_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sanitize_topic_input(text: str) -> str:
    cleaned = normalize_whitespace(strip_html_tags(text))
    for pattern in PII_PATTERNS:
        cleaned = re.sub(pattern, "[REDACTED]", cleaned)
    return cleaned


def contains_blocked_prompt_pattern(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in BLOCKED_PROMPT_PATTERNS)


def sanitize_ai_output_text(text: str) -> str:
    cleaned = normalize_whitespace(text)
    for pattern in PII_PATTERNS:
        cleaned = re.sub(pattern, "[REDACTED]", cleaned)
    return cleaned


def contains_blocked_output_pattern(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in OUTPUT_BLOCKED_PATTERNS)


def sanitize_ai_payload(payload: Any) -> Any:
    if isinstance(payload, str):
        cleaned = sanitize_ai_output_text(payload)
        if contains_blocked_output_pattern(cleaned):
            raise ValueError("Blocked unsafe content detected in AI output.")
        return cleaned
    if isinstance(payload, list):
        return [sanitize_ai_payload(item) for item in payload]
    if isinstance(payload, dict):
        return {key: sanitize_ai_payload(value) for key, value in payload.items()}
    return payload
