from __future__ import annotations

import pytest

from config import get_settings
from engine import mode_router, prompt_builder, response_formatter
from utils.helpers import AIResponseFormatError, InvalidModeError
from utils.validators import validate_lyrics_text


def test_validate_lyrics_text_trims_input() -> None:
    assert validate_lyrics_text("\n  hello from the chorus  \n") == "hello from the chorus"


def test_validate_lyrics_text_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        validate_lyrics_text("   ")


def test_validate_lyrics_text_rejects_long_input(monkeypatch) -> None:
    monkeypatch.setenv("MAX_LYRICS_LENGTH", "5")
    get_settings.cache_clear()

    with pytest.raises(ValueError, match="5 characters or fewer"):
        validate_lyrics_text("123456")


def test_route_mode_dispatches_to_registered_handler(monkeypatch) -> None:
    monkeypatch.setitem(
        mode_router.MODE_HANDLERS,
        "analyze",
        lambda payload: {"title": "Handled", "content": payload["lyrics"], "meta": {}},
    )

    result = mode_router.route_mode("analyze", {"lyrics": "Signal"})

    assert result["title"] == "Handled"
    assert result["content"] == "Signal"


def test_route_mode_rejects_unknown_mode() -> None:
    with pytest.raises(InvalidModeError):
        mode_router.route_mode("unknown", {"lyrics": "Signal"})


def test_build_compare_prompt_mentions_both_inputs() -> None:
    prompt = prompt_builder.build_compare_prompt("first lyric", "second lyric")

    assert "Song A Lyrics" in prompt
    assert "first lyric" in prompt
    assert "second lyric" in prompt
    assert "valid JSON only" in prompt


def test_format_analysis_response_parses_expected_payload() -> None:
    result = response_formatter.format_analysis_response(
        '{"meaning":"A search for hope","emotion":"Longing","theme":"Resilience","key_lines":["hold on"]}'
    )

    assert result.meaning == "A search for hope"
    assert result.key_lines == ["hold on"]


def test_format_analysis_response_rejects_invalid_json() -> None:
    with pytest.raises(AIResponseFormatError, match="not valid JSON"):
        response_formatter.format_analysis_response("not-json")
