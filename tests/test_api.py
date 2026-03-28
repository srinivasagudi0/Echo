from __future__ import annotations

import pytest

from config import get_settings
from engine import ai_client
from utils.helpers import AIUpstreamError


def test_root_serves_index(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["ui"] == "Streamlit"


def test_health_reports_configuration_status(client) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "ai_configured": True}


@pytest.mark.parametrize(
    ("path", "payload", "mock_response", "expected_title"),
    [
        ("/api/analyze", {"lyrics": "hello darkness"}, '{"meaning":"Reflection","emotion":"Melancholy","theme":"Isolation","key_lines":["hello darkness"]}', "Song Insight"),
        ("/api/remix", {"lyrics": "keep me standing"}, '{"remix":"Stand taller than the setback."}', "Remix Meaning"),
        ("/api/advice", {"lyrics": "if I leave now"}, '{"advice":"Make the hard choice before fear makes it for you."}', "Life Advice"),
        ("/api/story", {"lyrics": "the city wakes"}, '{"story":"The skyline glows as a runner crosses the bridge at sunrise."}', "Story Mode"),
    ],
)
def test_single_lyric_endpoints_return_cards(client, monkeypatch, path, payload, mock_response, expected_title) -> None:
    monkeypatch.setattr(ai_client, "call_ai", lambda prompt: mock_response)

    response = client.post(path, json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == expected_title
    assert body["content"]


def test_compare_endpoint_returns_card(client, monkeypatch) -> None:
    monkeypatch.setattr(
        ai_client,
        "call_ai",
        lambda prompt: '{"emotion_a":"Calm","emotion_b":"Restless","difference":"One settles while the other strains forward","verdict":"The contrast is patience versus urgency."}',
    )

    response = client.post("/api/compare", json={"lyrics_a": "stay still", "lyrics_b": "run now"})

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Song Comparison"
    assert body["meta"]["difference"] == "One settles while the other strains forward"


def test_blank_input_returns_structured_400(client) -> None:
    response = client.post("/api/analyze", json={"lyrics": "   "})

    assert response.status_code == 400
    body = response.json()
    assert body["code"] == "validation_error"
    assert body["errors"][0]["loc"] == "lyrics"


def test_over_limit_input_returns_structured_400(client, monkeypatch) -> None:
    monkeypatch.setenv("MAX_LYRICS_LENGTH", "5")
    get_settings.cache_clear()

    response = client.post("/api/analyze", json={"lyrics": "123456"})

    assert response.status_code == 400
    assert response.json()["code"] == "validation_error"


def test_malformed_ai_json_returns_502(client, monkeypatch) -> None:
    monkeypatch.setattr(ai_client, "call_ai", lambda prompt: "not-json")

    response = client.post("/api/analyze", json={"lyrics": "echoes"})

    assert response.status_code == 502
    assert response.json()["code"] == "ai_response_invalid"


def test_upstream_ai_failure_returns_502(client, monkeypatch) -> None:
    monkeypatch.setattr(ai_client, "call_ai", lambda prompt: (_ for _ in ()).throw(AIUpstreamError("OpenAI is down.")))

    response = client.post("/api/analyze", json={"lyrics": "echoes"})

    assert response.status_code == 502
    assert response.json()["detail"] == "OpenAI is down."


def test_missing_ai_configuration_returns_503(client, monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    get_settings.cache_clear()

    response = client.post("/api/analyze", json={"lyrics": "echoes"})

    assert response.status_code == 503
    assert response.json()["code"] == "ai_not_configured"
