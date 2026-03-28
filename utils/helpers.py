from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def normalize_error_location(location: tuple[Any, ...] | list[Any]) -> str:
    parts: list[str] = []
    for item in location:
        if item == "body":
            continue
        parts.append(str(item))
    return ".".join(parts) or "request"


def normalize_validation_errors(errors: list[dict[str, Any]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for error in errors:
        normalized.append(
            {
                "loc": normalize_error_location(error.get("loc", ())),
                "message": error.get("msg", "Invalid input."),
                "type": error.get("type", "value_error"),
            }
        )
    return normalized


@dataclass(slots=True)
class AppError(Exception):
    detail: str
    status_code: int = 500
    code: str = "app_error"
    errors: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"detail": self.detail, "code": self.code}
        if self.errors:
            payload["errors"] = self.errors
        return payload


class InvalidModeError(AppError):
    def __init__(self, mode: str) -> None:
        super().__init__(
            detail=f"Unsupported mode '{mode}'.",
            status_code=400,
            code="invalid_mode",
            errors=[{"loc": "mode", "message": "Choose a supported mode.", "type": "value_error"}],
        )


class AIConfigurationError(AppError):
    def __init__(self, detail: str = "OpenAI is not configured. Set OPENAI_API_KEY and OPENAI_MODEL.") -> None:
        super().__init__(detail=detail, status_code=503, code="ai_not_configured")


class AIUpstreamError(AppError):
    def __init__(self, detail: str, *, errors: list[dict[str, Any]] | None = None) -> None:
        super().__init__(detail=detail, status_code=502, code="ai_upstream_error", errors=errors or [])


class AIResponseFormatError(AppError):
    def __init__(self, detail: str, *, errors: list[dict[str, Any]] | None = None) -> None:
        super().__init__(detail=detail, status_code=502, code="ai_response_invalid", errors=errors or [])
