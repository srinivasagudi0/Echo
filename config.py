from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


def _read_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default

    try:
        return float(raw)
    except ValueError:
        return default


def _read_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default

    try:
        return int(raw)
    except ValueError:
        return default


@dataclass(frozen=True, slots=True)
class Settings:
    openai_api_key: str | None
    openai_model: str | None
    openai_base_url: str | None
    openai_timeout: float
    max_lyrics_length: int

    @property
    def ai_configured(self) -> bool:
        return bool(self.openai_api_key and self.openai_model)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL"),
        openai_base_url=os.getenv("OPENAI_BASE_URL"),
        openai_timeout=_read_float("OPENAI_TIMEOUT", 30.0),
        max_lyrics_length=_read_int("MAX_LYRICS_LENGTH", 5000),
    )
