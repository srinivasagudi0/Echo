from __future__ import annotations

from engine import ai_client
from modes.life_advice import lyric_advice
from modes.lyric_converter import analyze_lyrics
from modes.remix_meaning import remix_meaning
from modes.song_compare import compare_songs
from modes.story_mode import story_mode


def test_analyze_lyrics_returns_card(monkeypatch) -> None:
    monkeypatch.setattr(
        ai_client,
        "call_ai",
        lambda prompt: '{"meaning":"A late-night confession","emotion":"Tender","theme":"Vulnerability","key_lines":["stay with me"]}',
    )

    result = analyze_lyrics("stay with me")

    assert result["title"] == "Song Insight"
    assert result["content"] == "A late-night confession"
    assert result["meta"]["emotion"] == "Tender"


def test_compare_songs_returns_card(monkeypatch) -> None:
    monkeypatch.setattr(
        ai_client,
        "call_ai",
        lambda prompt: '{"emotion_a":"Hopeful","emotion_b":"Defiant","difference":"One reaches out while the other pushes back","verdict":"The songs move in opposite emotional directions."}',
    )

    result = compare_songs("we can make it", "leave me alone")

    assert result["title"] == "Song Comparison"
    assert result["content"] == "The songs move in opposite emotional directions."
    assert result["meta"]["emotion_a"] == "Hopeful"


def test_remix_meaning_returns_card(monkeypatch) -> None:
    monkeypatch.setattr(ai_client, "call_ai", lambda prompt: '{"remix":"Keep moving forward even when the room goes dark."}')

    result = remix_meaning("the lights went out")

    assert result["title"] == "Remix Meaning"
    assert "Keep moving forward" in result["content"]


def test_lyric_advice_returns_card(monkeypatch) -> None:
    monkeypatch.setattr(ai_client, "call_ai", lambda prompt: '{"advice":"Say what matters before the moment disappears."}')

    result = lyric_advice("time keeps slipping")

    assert result["title"] == "Life Advice"
    assert result["content"] == "Say what matters before the moment disappears."


def test_story_mode_returns_shared_card_shape(monkeypatch) -> None:
    monkeypatch.setattr(
        ai_client,
        "call_ai",
        lambda prompt: '{"story":"A singer walks through the city at dawn, finally deciding to start again."}',
    )

    result = story_mode("new day rising")

    assert result["title"] == "Story Mode"
    assert result["content"].startswith("A singer walks")
    assert result["meta"] == {}
