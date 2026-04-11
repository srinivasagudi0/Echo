from __future__ import annotations

import streamlit as st

from engine.mode_router import route_mode


st.title("ECHO - Hear what the lyrics are really saying.")

mode = st.selectbox("Select mode", ["🧐 Analyze", "🎀 Compare", "🌹 Remix", "✨ Advice", "☁️ Story"])

if mode == "🧐 Analyze":
    lyrics = st.text_area("Enter song lyrics")
    if st.button("Analyze"):
        try:
            result = route_mode("analyze", {"lyrics": lyrics})
            st.subheader(result["title"])
            st.write(result["content"])
        except Exception as error:
            st.error(str(error))
elif mode == "🎀 Compare":
    lyrics_a = st.text_area("Enter first song lyrics")
    lyrics_b = st.text_area("Enter second song lyrics")
    if st.button("Compare"):
        try:
            result = route_mode("compare", {"lyrics_a": lyrics_a, "lyrics_b": lyrics_b})
            st.subheader(result["title"])
            st.write(result["content"])
        except Exception as error:
            st.error(str(error))
elif mode == "🌹 Remix":
    lyrics = st.text_area("Enter song lyrics")
    if st.button("Remix"):
        try:
            result = route_mode("remix", {"lyrics": lyrics})
            st.subheader(result["title"])
            st.write(result["content"])
        except Exception as error:
            st.error(str(error))
elif mode == "✨ Advice":
    lyrics = st.text_area("Enter song lyrics")
    if st.button("Get Advice"):
        try:
            result = route_mode("advice", {"lyrics": lyrics})
            st.subheader(result["title"])
            st.write(result["content"])
        except Exception as error:
            st.error(str(error))
elif mode == "☁️ Story":
    lyrics = st.text_area("Enter song lyrics")
    if st.button("Generate Story"):
        try:
            result = route_mode("story", {"lyrics": lyrics})
            st.subheader(result["title"])
            st.write(result["content"])
        except Exception as error:
            st.error(str(error))
