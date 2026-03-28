from __future__ import annotations

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

from config import get_settings
from utils.helpers import AIConfigurationError, AIUpstreamError
from utils.text_cleaner import clean_model_json


SYSTEM_PROMPT = (
    "You are Echo, a lyric analysis assistant. "
    "Always follow the requested JSON schema exactly and avoid any markdown."
)


def is_ai_configured() -> bool:
    return get_settings().ai_configured


def _build_client() -> OpenAI:
    settings = get_settings()
    if not settings.ai_configured:
        raise AIConfigurationError()

    client_kwargs = {
        "api_key": settings.openai_api_key,
        "timeout": settings.openai_timeout,
    }
    if settings.openai_base_url:
        client_kwargs["base_url"] = settings.openai_base_url

    return OpenAI(**client_kwargs)


def call_ai(prompt: str, *, system_prompt: str = SYSTEM_PROMPT) -> str:
    settings = get_settings()
    if not settings.ai_configured:
        raise AIConfigurationError()

    client = _build_client()
    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
    except (APITimeoutError, APIConnectionError) as exc:
        raise AIUpstreamError(
            "The OpenAI request failed before a response was received.",
            errors=[{"loc": "openai", "message": str(exc), "type": exc.__class__.__name__}],
        ) from exc
    except APIStatusError as exc:
        raise AIUpstreamError(
            f"OpenAI returned status {exc.status_code}.",
            errors=[{"loc": "openai", "message": str(exc), "type": exc.__class__.__name__}],
        ) from exc
    except Exception as exc:
        raise AIUpstreamError(
            "An unexpected OpenAI client error occurred.",
            errors=[{"loc": "openai", "message": str(exc), "type": exc.__class__.__name__}],
        ) from exc

    try:
        content = response.choices[0].message.content or ""
    except (AttributeError, IndexError) as exc:
        raise AIUpstreamError(
            "OpenAI returned an unusable response payload.",
            errors=[{"loc": "openai", "message": str(exc), "type": exc.__class__.__name__}],
        ) from exc

    cleaned = clean_model_json(content)
    if not cleaned:
        raise AIUpstreamError(
            "OpenAI returned an empty response.",
            errors=[{"loc": "openai", "message": "No response content.", "type": "empty_response"}],
        )

    return cleaned
