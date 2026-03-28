from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from utils.validators import validate_key_lines, validate_response_text


class AnalysisResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    meaning: str
    emotion: str
    theme: str
    key_lines: list[str] = Field(default_factory=list)

    @field_validator("meaning", "emotion", "theme")
    @classmethod
    def normalize_text_fields(cls, value: str, info) -> str:
        return validate_response_text(value, field_name=info.field_name)

    @field_validator("key_lines")
    @classmethod
    def normalize_key_lines(cls, value: list[str]) -> list[str]:
        return validate_key_lines(value)


class AdviceResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    advice: str

    @field_validator("advice")
    @classmethod
    def normalize_advice(cls, value: str) -> str:
        return validate_response_text(value, field_name="advice")


class RemixResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    remix: str

    @field_validator("remix")
    @classmethod
    def normalize_remix(cls, value: str) -> str:
        return validate_response_text(value, field_name="remix")


class StoryResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    story: str

    @field_validator("story")
    @classmethod
    def normalize_story(cls, value: str) -> str:
        return validate_response_text(value, field_name="story")
