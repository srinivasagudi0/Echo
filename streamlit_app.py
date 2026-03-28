from __future__ import annotations

from html import escape
from typing import Any

import streamlit as st
from pydantic import ValidationError

from engine.ai_client import is_ai_configured
from engine.mode_router import route_mode
from models.song import CompareRequest, LyricsRequest
from utils.helpers import AppError


MODE_CONFIG = {
    "analyze": {
        "label": "Analyze",
        "emoji": "💌",
        "title": "Hear what the lyrics are really saying.",
        "description": "Decode the emotional core, meaning, theme, and key lines inside any lyric excerpt.",
        "submit_label": "Analyze Lyrics",
        "single_input_label": "Lyrics",
        "single_input_placeholder": "Paste a verse, chorus, or full lyric excerpt...",
    },
    "compare": {
        "label": "Compare",
        "emoji": "🎀",
        "title": "Put two songs in emotional conversation.",
        "description": "Contrast two lyric excerpts and surface the difference in tone, message, and emotional weight.",
        "submit_label": "Compare Lyrics",
    },
    "remix": {
        "label": "Remix",
        "emoji": "🌷",
        "title": "Turn raw emotion into a motivational rewrite.",
        "description": "Keep the meaning, sharpen the energy, and recast the lyrics as a forward-driving message.",
        "submit_label": "Remix Meaning",
        "single_input_label": "Lyrics",
        "single_input_placeholder": "Paste the lyrics you want transformed...",
    },
    "advice": {
        "label": "Advice",
        "emoji": "✨",
        "title": "Convert lyrics into practical life advice.",
        "description": "Pull out the lesson hidden in the song and reframe it into direct guidance you can act on.",
        "submit_label": "Get Advice",
        "single_input_label": "Lyrics",
        "single_input_placeholder": "Paste the lyrics you want interpreted as advice...",
    },
    "story": {
        "label": "Story",
        "emoji": "☁️",
        "title": "Let the lyrics unfold as a cinematic scene.",
        "description": "Transform a lyric excerpt into a short narrative with atmosphere, motion, and a clear emotional arc.",
        "submit_label": "Generate Story",
        "single_input_label": "Lyrics",
        "single_input_placeholder": "Paste the lyrics you want turned into a story...",
    },
}


def validate_payload(mode: str, payload: dict[str, Any]) -> dict[str, Any]:
    if mode == "compare":
        return CompareRequest.model_validate(payload).model_dump()
    return LyricsRequest.model_validate(payload).model_dump()


def format_app_error(error: Exception) -> str:
    if isinstance(error, AppError):
        if error.errors:
            return f"{error.detail} {error.errors[0].get('message', '')}".strip()
        return error.detail

    if isinstance(error, ValidationError):
        first_error = error.errors(include_url=False)[0]
        return first_error.get("msg", "Validation failed.")

    return "Something went wrong while processing the lyrics."


def render_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');
        :root {
          --echo-cream: #fff8f4;
          --echo-blush: #ffd8e6;
          --echo-petal: #ffc4da;
          --echo-lemon: #ffe8a3;
          --echo-mint: #bdebdc;
          --echo-lilac: #d8d4ff;
          --echo-ink: #3f355b;
          --echo-ink-soft: #6f618d;
          --echo-berry: #ec6f98;
          --echo-berry-deep: #d94f7f;
          --echo-border: rgba(126, 96, 162, 0.16);
          --echo-shadow: 0 24px 60px rgba(151, 121, 183, 0.16);
        }
        .stApp {
          font-family: "DM Sans", sans-serif;
          background:
            radial-gradient(circle at 10% 10%, rgba(255, 196, 218, 0.8), transparent 20%),
            radial-gradient(circle at 92% 18%, rgba(216, 212, 255, 0.85), transparent 24%),
            radial-gradient(circle at 85% 82%, rgba(189, 235, 220, 0.8), transparent 20%),
            linear-gradient(165deg, #fffaf7 0%, #fff0f5 46%, #fff8da 100%);
        }
        [data-testid="stAppViewContainer"] {
          overflow-x: hidden;
        }
        .block-container {
          max-width: 1140px;
          padding-top: 2rem;
          padding-bottom: 3.5rem;
          padding-left: 1.2rem;
          padding-right: 1.2rem;
        }
        section[data-testid="stSidebar"] {
          background:
            linear-gradient(180deg, rgba(255,255,255,0.82) 0%, rgba(255,243,248,0.94) 100%);
          border-right: 1px solid rgba(255,255,255,0.65);
          backdrop-filter: blur(24px);
        }
        section[data-testid="stSidebar"] * {
          color: var(--echo-ink);
          font-family: "DM Sans", sans-serif;
        }
        .stRadio > label,
        .stTextArea label,
        .stMarkdown,
        .stCaption,
        .stAlert {
          font-family: "DM Sans", sans-serif;
        }
        .stApp,
        .stApp p,
        .stApp li,
        .stApp label,
        .stApp span,
        [data-testid="stWidgetLabel"] *,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        .stAlert p {
          color: var(--echo-ink) !important;
        }
        [data-testid="stTextAreaRootElement"] label p,
        [data-testid="stMarkdownContainer"] ul,
        [data-testid="stMarkdownContainer"] ol {
          color: var(--echo-ink) !important;
        }
        .stTextArea textarea {
          border-radius: 22px !important;
          border: 1px solid var(--echo-border) !important;
          background: rgba(255, 255, 255, 0.94) !important;
          color: var(--echo-ink) !important;
          font-size: 1rem !important;
          line-height: 1.6 !important;
          box-shadow: inset 0 1px 0 rgba(255,255,255,0.6);
        }
        .stTextArea textarea:focus {
          border-color: rgba(236, 111, 152, 0.58) !important;
          box-shadow: 0 0 0 1px rgba(236, 111, 152, 0.12) !important;
        }
        .stButton > button,
        .stForm button[kind="primary"] {
          border-radius: 999px !important;
          border: none !important;
          min-height: 3rem !important;
          font-weight: 800 !important;
          background: linear-gradient(135deg, var(--echo-berry) 0%, var(--echo-berry-deep) 100%) !important;
          color: white !important;
          box-shadow: 0 14px 30px rgba(236, 111, 152, 0.24) !important;
        }
        button[kind="segmented_control"],
        [data-testid="stPills"] button {
          border-radius: 999px !important;
          border: 1px solid rgba(217, 79, 127, 0.14) !important;
          background: rgba(255,255,255,0.92) !important;
          color: var(--echo-ink) !important;
          font-weight: 700 !important;
        }
        button[kind="segmented_control"][aria-selected="true"],
        [data-testid="stPills"] button[aria-selected="true"] {
          background: linear-gradient(135deg, rgba(255, 225, 236, 0.98) 0%, rgba(255, 239, 182, 0.95) 100%) !important;
          color: var(--echo-ink) !important;
          border-color: rgba(217, 79, 127, 0.28) !important;
          box-shadow: 0 10px 22px rgba(236, 111, 152, 0.16) !important;
        }
        [data-testid="stSegmentedControl"] {
          margin-bottom: 0.35rem;
        }
        .stSpinner > div {
          border-top-color: var(--echo-berry) !important;
        }
        .echo-hero {
          padding: 2.2rem 2.25rem;
          border-radius: 30px;
          color: var(--echo-ink);
          background:
            radial-gradient(circle at top right, rgba(255,255,255,0.74), transparent 34%),
            linear-gradient(135deg, rgba(255,255,255,0.92) 0%, rgba(255, 237, 244, 0.96) 56%, rgba(255, 248, 212, 0.95) 100%);
          border: 1px solid rgba(255,255,255,0.7);
          box-shadow: var(--echo-shadow);
        }
        .echo-eyebrow {
          margin: 0 0 0.8rem;
          letter-spacing: 0.18em;
          font-size: 0.78rem;
          font-weight: 800;
          color: var(--echo-ink-soft);
        }
        .echo-hero h1 {
          margin: 0;
          font-family: "Fraunces", serif;
          font-size: clamp(2.3rem, 4vw, 4.1rem);
          line-height: 0.98;
          letter-spacing: -0.04em;
        }
        .echo-hero p {
          margin: 1rem 0 0;
          font-size: 1rem;
          line-height: 1.7;
          max-width: 38rem;
          color: var(--echo-ink-soft);
        }
        .echo-note {
          padding: 1.35rem;
          border-radius: 26px;
          background: rgba(255,255,255,0.86);
          border: 1px solid rgba(255,255,255,0.72);
          box-shadow: var(--echo-shadow);
          height: 100%;
        }
        .echo-note h3 {
          margin: 0 0 0.4rem;
          font-family: "Fraunces", serif;
          font-size: 1.2rem;
          color: var(--echo-ink);
        }
        .echo-note p,
        .echo-note li {
          color: var(--echo-ink-soft);
          line-height: 1.6;
        }
        .echo-status {
          padding: 1rem 1.1rem;
          border-radius: 24px;
          background: rgba(255, 255, 255, 0.88);
          border: 1px solid var(--echo-border);
          color: var(--echo-ink);
          margin-bottom: 1rem;
          box-shadow: 0 16px 34px rgba(151, 121, 183, 0.1);
        }
        .echo-status strong {
          display: block;
          margin-bottom: 0.2rem;
        }
        .echo-status small {
          color: var(--echo-ink-soft);
        }
        .echo-panel {
          padding: 1.35rem 1.35rem 1rem;
          border-radius: 28px;
          background: rgba(255,255,255,0.86);
          border: 1px solid rgba(255,255,255,0.72);
          box-shadow: var(--echo-shadow);
        }
        .echo-form-title {
          margin: 0 0 0.25rem;
          font-family: "Fraunces", serif;
          font-size: 1.4rem;
          color: var(--echo-ink) !important;
        }
        .echo-form-copy {
          margin: 0 0 1rem;
          color: var(--echo-ink-soft) !important;
          line-height: 1.6;
        }
        .echo-card {
          padding: 1.35rem 1.4rem;
          border-radius: 28px;
          background: linear-gradient(180deg, rgba(255,255,255,0.86) 0%, rgba(255, 244, 248, 0.9) 100%);
          border: 1px solid rgba(255,255,255,0.78);
          box-shadow: var(--echo-shadow);
        }
        .echo-card h3 {
          margin: 0 0 0.6rem;
          font-family: "Fraunces", serif;
          font-size: 1.6rem;
          color: var(--echo-ink);
        }
        .echo-card p {
          color: var(--echo-ink-soft);
          line-height: 1.72;
        }
        .echo-section-label {
          margin: 0 0 0.55rem;
          font-size: 0.86rem;
          font-weight: 800;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          color: var(--echo-ink-soft) !important;
        }
        .echo-ribbon {
          display: inline-flex;
          align-items: center;
          gap: 0.45rem;
          margin-bottom: 0.85rem;
          padding: 0.45rem 0.8rem;
          border-radius: 999px;
          background: linear-gradient(135deg, rgba(255, 225, 236, 0.96) 0%, rgba(255, 239, 182, 0.95) 100%);
          color: var(--echo-ink);
          font-size: 0.85rem;
          font-weight: 700;
        }
        .echo-meta {
          margin-top: 1rem;
          padding-top: 1rem;
          border-top: 1px dashed rgba(126, 96, 162, 0.2);
        }
        .echo-meta-label {
          display: inline-block;
          font-size: 0.78rem;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          color: var(--echo-ink-soft);
          margin-bottom: 0.4rem;
        }
        .echo-meta-card {
          padding: 0.95rem 1rem;
          height: 100%;
          border-radius: 20px;
          background: rgba(255,255,255,0.72);
          border: 1px solid rgba(126, 96, 162, 0.1);
        }
        .echo-meta-card p,
        .echo-meta-card ul,
        .echo-meta-card li {
          margin: 0;
          color: var(--echo-ink-soft) !important;
          line-height: 1.6;
        }
        .echo-meta-card ul {
          padding-left: 1rem;
          margin-top: 0.2rem;
        }
        @media (max-width: 900px) {
          .block-container {
            padding-left: 0.9rem;
            padding-right: 0.9rem;
          }
        }
        @media (max-width: 640px) {
          .echo-hero,
          .echo-note,
          .echo-panel,
          .echo-card {
            border-radius: 22px;
          }
          .echo-hero {
            padding: 1.4rem;
          }
          .echo-hero h1 {
            font-size: 2.2rem;
          }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## ECHO")
        st.caption("A soft little lyric studio.")

        status_copy = "OpenAI configured" if is_ai_configured() else "OpenAI key or model missing"
        st.markdown(
            f"""
            <div class="echo-status">
              <strong>System Status</strong>
              {status_copy}<br />
              <small>{'Ready to read your lyrics.' if is_ai_configured() else 'Add your key and model to wake Echo up.'}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Input Rules")
        st.write("- Paste lyric text directly")
        st.write("- Compare mode requires two excerpts")
        st.write("- Empty input is rejected before the model call")
        st.write("- Shorter snippets usually give sharper results")


def render_header(config: dict[str, str]) -> None:
    hero_column, note_column = st.columns([1.5, 0.95], gap="medium")

    with hero_column:
        st.markdown(
            f"""
            <section class="echo-hero">
              <p class="echo-eyebrow">{escape(config["emoji"])} LYRIC INTELLIGENCE</p>
              <h1>{escape(config["title"])}</h1>
              <p>{escape(config["description"])}</p>
            </section>
            """,
            unsafe_allow_html=True,
        )

    with note_column:
        st.markdown(
            """
            <aside class="echo-note">
              <h3>Sweet spot</h3>
              <p>Short verses and choruses usually produce the clearest read. If a result feels broad, trim the input to the lines doing the emotional heavy lifting.</p>
              <ul>
                <li>Use compare for contrast</li>
                <li>Use remix for uplifting rewrites</li>
                <li>Use story when you want atmosphere</li>
              </ul>
            </aside>
            """,
            unsafe_allow_html=True,
        )


def render_meta_content(value: Any) -> str:
    if isinstance(value, list):
        items = "".join(f"<li>{escape(str(item))}</li>" for item in value)
        return f"<ul>{items}</ul>"
    return f"<p>{escape(str(value))}</p>"


def render_result(card: dict[str, Any]) -> None:
    st.markdown(
        f"""
        <div class="echo-card">
          <div class="echo-ribbon">💗 Echo Result</div>
          <h3>{escape(card["title"])}</h3>
          <p>{escape(card["content"])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    meta = {key: value for key, value in card.get("meta", {}).items() if value}
    if not meta:
        return

    columns = st.columns(len(meta))
    for column, (key, value) in zip(columns, meta.items(), strict=False):
        label = key.replace("_", " ").title()
        with column:
            st.markdown(
                f"""
                <div class="echo-meta-card">
                  <span class="echo-meta-label">{escape(label)}</span>
                  {render_meta_content(value)}
                </div>
                """,
                unsafe_allow_html=True,
            )


def main() -> None:
    st.set_page_config(page_title="Echo", page_icon="🎧", layout="wide")
    render_styles()

    render_sidebar()
    mode = st.pills(
        "Choose a mode",
        options=list(MODE_CONFIG.keys()),
        selection_mode="single",
        default=st.session_state.get("echo_mode", "analyze"),
        format_func=lambda mode_id: f'{MODE_CONFIG[mode_id]["emoji"]} {MODE_CONFIG[mode_id]["label"]}',
        width="stretch",
    )
    if mode is None:
        mode = st.session_state.get("echo_mode", "analyze")
    if st.session_state.get("echo_mode") != mode:
        st.session_state["echo_mode"] = mode
        st.session_state["echo_result"] = None
        st.session_state["echo_error"] = None

    config = MODE_CONFIG[mode]
    render_header(config)

    st.markdown('<p class="echo-section-label">Paste lyrics and run Echo</p>', unsafe_allow_html=True)
    form_container = st.container()
    with form_container:
        st.markdown(
            """
            <div class="echo-panel">
              <h3 class="echo-form-title">Make it sing</h3>
              <p class="echo-form-copy">Paste a lyric excerpt below, then run the mode you picked above. Echo will keep the result in view until you switch modes or submit again.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with st.form("echo-form", clear_on_submit=False):
        if mode == "compare":
            left, right = st.columns(2)
            with left:
                lyrics_a = st.text_area(
                    "Song A Lyrics",
                    placeholder="Paste the first lyric excerpt...",
                    height=220,
                )
            with right:
                lyrics_b = st.text_area(
                    "Song B Lyrics",
                    placeholder="Paste the second lyric excerpt...",
                    height=220,
                )
            payload = {"lyrics_a": lyrics_a, "lyrics_b": lyrics_b}
        else:
            lyrics = st.text_area(
                config["single_input_label"],
                placeholder=config["single_input_placeholder"],
                height=260,
            )
            payload = {"lyrics": lyrics}

        submitted = st.form_submit_button(config["submit_label"], type="primary", use_container_width=True)

    if submitted:
        try:
            validated_payload = validate_payload(mode, payload)
            with st.spinner("Listening for the signal in the lyrics..."):
                card = route_mode(mode, validated_payload)
            st.session_state["echo_result"] = card
            st.session_state["echo_error"] = None
        except (AppError, ValidationError) as error:
            st.session_state["echo_error"] = format_app_error(error)
            st.session_state["echo_result"] = None

    if st.session_state.get("echo_error"):
        st.error(st.session_state["echo_error"])

    if st.session_state.get("echo_result"):
        render_result(st.session_state["echo_result"])


if __name__ == "__main__":
    main()
