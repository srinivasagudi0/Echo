from __future__ import annotations

import pytest
from pydantic import ValidationError

from streamlit_app import format_app_error, validate_payload
from utils.helpers import AIUpstreamError


def test_validate_payload_for_single_input_mode() -> None:
    payload = validate_payload("analyze", {"lyrics": "  signal in the static  "})

    assert payload == {"lyrics": "signal in the static"}


def test_validate_payload_for_compare_mode() -> None:
    payload = validate_payload("compare", {"lyrics_a": " one ", "lyrics_b": " two "})

    assert payload == {"lyrics_a": "one", "lyrics_b": "two"}


def test_validate_payload_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        validate_payload("story", {"lyrics": "   "})


def test_format_app_error_uses_first_nested_message() -> None:
    error = AIUpstreamError("OpenAI failed.", errors=[{"message": "Gateway timeout."}])

    assert format_app_error(error) == "OpenAI failed. Gateway timeout."
