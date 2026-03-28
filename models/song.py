from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from utils.validators import validate_lyrics_text, validate_response_text


class LyricsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lyrics: str

    @field_validator("lyrics")
    @classmethod
    def normalize_lyrics(cls, value: str) -> str:
        return validate_lyrics_text(value, field_name="lyrics")


class CompareRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lyrics_a: str
    lyrics_b: str

    @field_validator("lyrics_a")
    @classmethod
    def normalize_lyrics_a(cls, value: str) -> str:
        return validate_lyrics_text(value, field_name="lyrics_a")

    @field_validator("lyrics_b")
    @classmethod
    def normalize_lyrics_b(cls, value: str) -> str:
        return validate_lyrics_text(value, field_name="lyrics_b")


class CardResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    content: str
    meta: dict[str, Any] = Field(default_factory=dict)

    @field_validator("title", "content")
    @classmethod
    def normalize_text_fields(cls, value: str, info) -> str:
        return validate_response_text(value, field_name=info.field_name)


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"] = "ok"
    ai_configured: bool


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    detail: str
    code: str | None = None
    errors: list[dict[str, Any]] | None = None
