from __future__ import annotations

import re
from typing import Any


CODE_FENCE_PATTERN = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE)


def normalize_whitespace(text: str) -> str:
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def strip_code_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = CODE_FENCE_PATTERN.sub("", stripped).strip()
    return stripped


def clean_model_json(text: str) -> str:
    return strip_code_fences(text).strip()


def clean_meta(value: Any) -> Any:
    if isinstance(value, str):
        return normalize_whitespace(value)
    if isinstance(value, list):
        return [clean_meta(item) for item in value if item not in (None, "", [])]
    if isinstance(value, dict):
        return {key: clean_meta(item) for key, item in value.items()}
    return value
