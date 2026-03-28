from __future__ import annotations

from textwrap import dedent


JSON_INSTRUCTIONS = "Respond with valid JSON only. Do not wrap the JSON in markdown and do not add extra keys."


def build_analysis_prompt(lyrics: str) -> str:
    return dedent(
        f"""
        Analyze the emotional meaning of these song lyrics.

        Return JSON with this shape:
        {{
          "meaning": "Brief explanation of the overall meaning",
          "emotion": "Primary emotion in a few words",
          "theme": "Main lyrical theme",
          "key_lines": ["Up to three short lyric excerpts that support the analysis"]
        }}

        {JSON_INSTRUCTIONS}

        Lyrics:
        {lyrics}
        """
    ).strip()


def build_compare_prompt(lyrics_a: str, lyrics_b: str) -> str:
    return dedent(
        f"""
        Compare the emotional tone and message of these two lyric excerpts.

        Return JSON with this shape:
        {{
          "emotion_a": "Emotion for Song A",
          "emotion_b": "Emotion for Song B",
          "difference": "Main contrast between the songs",
          "verdict": "Short comparative takeaway"
        }}

        {JSON_INSTRUCTIONS}

        Song A Lyrics:
        {lyrics_a}

        Song B Lyrics:
        {lyrics_b}
        """
    ).strip()


def build_remix_prompt(lyrics: str) -> str:
    return dedent(
        f"""
        Rewrite these lyrics as a motivational message while preserving the core idea.

        Return JSON with this shape:
        {{
          "remix": "Motivational rewrite"
        }}

        {JSON_INSTRUCTIONS}

        Lyrics:
        {lyrics}
        """
    ).strip()


def build_advice_prompt(lyrics: str) -> str:
    return dedent(
        f"""
        Read these song lyrics and turn their message into practical life advice.

        Return JSON with this shape:
        {{
          "advice": "Concise, actionable life advice"
        }}

        {JSON_INSTRUCTIONS}

        Lyrics:
        {lyrics}
        """
    ).strip()


def build_story_prompt(lyrics: str) -> str:
    return dedent(
        f"""
        Turn these song lyrics into a short cinematic story.

        Return JSON with this shape:
        {{
          "story": "Short vivid story inspired by the lyrics"
        }}

        {JSON_INSTRUCTIONS}

        Lyrics:
        {lyrics}
        """
    ).strip()
