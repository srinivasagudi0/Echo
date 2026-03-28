from engine import ai_client, prompt_builder, response_formatter

def compare_songs(a, b):
    raw = ai_client.call_ai(prompt_builder.build_compare_prompt(a, b))
    data = response_formatter.format_compare_response(raw)

    return {
        "title": "Song Comparison",
        "content": data.verdict,
        "meta": data.model_dump()
    }
