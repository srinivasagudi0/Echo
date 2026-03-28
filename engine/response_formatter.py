from __future__ import annotations

import json
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from models.analysis import AdviceResult, AnalysisResult, RemixResult, StoryResult
from models.comparison import ComparisonResult
from utils.helpers import AIResponseFormatError, normalize_validation_errors
from utils.text_cleaner import clean_meta, clean_model_json


ModelT = TypeVar("ModelT", bound=BaseModel)


def _parse_json_object(raw: str) -> dict:
    cleaned = clean_model_json(raw)
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AIResponseFormatError(
            "The AI response was not valid JSON.",
            errors=[{"loc": "response", "message": str(exc), "type": "json_decode_error"}],
        ) from exc

    if not isinstance(payload, dict):
        raise AIResponseFormatError(
            "The AI response must be a JSON object.",
            errors=[{"loc": "response", "message": "Expected a JSON object.", "type": "type_error"}],
        )

    return payload


def _validate_payload(raw: str, schema: type[ModelT]) -> ModelT:
    payload = _parse_json_object(raw)
    try:
        result = schema.model_validate(payload)
    except ValidationError as exc:
        raise AIResponseFormatError(
            "The AI response did not match the expected schema.",
            errors=normalize_validation_errors(exc.errors(include_url=False)),
        ) from exc

    return result


def format_analysis_response(raw: str) -> AnalysisResult:
    result = _validate_payload(raw, AnalysisResult)
    result.key_lines = clean_meta(result.key_lines)
    return result


def format_compare_response(raw: str) -> ComparisonResult:
    return _validate_payload(raw, ComparisonResult)


def format_remix_response(raw: str) -> RemixResult:
    return _validate_payload(raw, RemixResult)


def format_advice_response(raw: str) -> AdviceResult:
    return _validate_payload(raw, AdviceResult)


def format_story_response(raw: str) -> StoryResult:
    return _validate_payload(raw, StoryResult)
