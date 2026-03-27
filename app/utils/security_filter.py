import re
import logging
from typing import Any
from app.core.exceptions import AppError

logger = logging.getLogger(__name__)

# PII Patterns: Email, International Phone, SSN, Credit Card
PII_PATTERNS = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "phone": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card": r"\b(?:\d[\s-]*?){13,16}\b",
}

# Injection Patterns: Heuristics for "jailbreak" or "ignore" style prompts
INJECTION_PATTERNS = [
    r"ignore (?:all )?previous instructions",
    r"you are now (?:a|an)",
    r"system:",
    r"\[system\]",
    r"user:",
    r"\[user\]",
    r"assistant:",
    r"### instruction",
]

class SecurityFilter:
    """
    Utility to scan and sanitize text for PII leakage and prompt injection attempts.
    """
    @staticmethod
    def strip_html_tags(text: str) -> str:
        return re.sub(r"<[^>]+>", "", text)

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def filter_input(text: str) -> str:
        """
        Scans input text for injection patterns. 
        Calculates a 'risk score' or simply raises an AppError for clear violations.
        """
        if not text:
            return text

        # Strip HTML and normalize whitespace BEFORE checking patterns
        cleaned = SecurityFilter.normalize_whitespace(SecurityFilter.strip_html_tags(text))
        
        lowered = cleaned.lower()
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, lowered):
                logger.warning(f"Security: Blocked potential injection pattern: {pattern}")
                raise AppError(
                    status_code=400,
                    code="UNSAFE_CONTENT",
                    message="The provided input contains patterns that are restricted for security reasons."
                )
        
        # Redact PII from input
        return SecurityFilter.redact_pii(cleaned)

    @staticmethod
    def filter_output(payload: Any) -> Any:
        """
        Deep-scans a JSON-compatible payload (dict, list, str) to redact PII.
        """
        if isinstance(payload, str):
            return SecurityFilter.redact_pii(payload)
        if isinstance(payload, list):
            return [SecurityFilter.filter_output(item) for item in payload]
        if isinstance(payload, dict):
            return {k: SecurityFilter.filter_output(v) for k, v in payload.items()}
        return payload

    @staticmethod
    def redact_pii(text: str) -> str:
        """
        Replaces detected PII with [REDACTED].
        """
        if not text:
            return text
            
        cleaned = text
        for label, pattern in PII_PATTERNS.items():
            matches = re.findall(pattern, cleaned)
            if matches:
                 logger.info(f"Security: Redacting {len(matches)} occurrences of {label}")
                 cleaned = re.sub(pattern, "[REDACTED]", cleaned)
        return cleaned

# Singleton instance
security_filter = SecurityFilter()
