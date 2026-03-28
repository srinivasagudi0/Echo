from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator

from utils.validators import validate_response_text


class ComparisonResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    emotion_a: str
    emotion_b: str
    difference: str
    verdict: str

    @field_validator("emotion_a", "emotion_b", "difference", "verdict")
    @classmethod
    def normalize_text_fields(cls, value: str, info) -> str:
        return validate_response_text(value, field_name=info.field_name)
