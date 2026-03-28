from __future__ import annotations

from config import get_settings
from utils.text_cleaner import normalize_whitespace


def validate_lyrics_text(value: str, *, field_name: str = "lyrics") -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string.")

    cleaned = normalize_whitespace(value)
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty.")

    max_length = get_settings().max_lyrics_length
    if len(cleaned) > max_length:
        raise ValueError(f"{field_name} must be {max_length} characters or fewer.")

    return cleaned


def validate_response_text(value: str, *, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string.")

    cleaned = normalize_whitespace(value)
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty.")
    return cleaned


def validate_key_lines(value: list[str]) -> list[str]:
    if not isinstance(value, list):
        raise ValueError("key_lines must be a list of strings.")

    cleaned: list[str] = []
    for line in value[:5]:
        if not isinstance(line, str):
            continue
        normalized = normalize_whitespace(line)
        if normalized:
            cleaned.append(normalized)

    return cleaned
