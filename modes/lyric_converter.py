from engine import ai_client, prompt_builder, response_formatter

def analyze_lyrics(lyrics):
    raw = ai_client.call_ai(prompt_builder.build_analysis_prompt(lyrics))
    data = response_formatter.format_analysis_response(raw)

    return {
        "title": "Song Insight",
        "content": data.meaning,
        "meta": {
            "emotion": data.emotion,
            "theme": data.theme,
            "key_lines": data.key_lines,
        }
    }
