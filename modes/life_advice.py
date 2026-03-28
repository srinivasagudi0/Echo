from engine import ai_client, prompt_builder, response_formatter


def lyric_advice(lyrics):
    raw = ai_client.call_ai(prompt_builder.build_advice_prompt(lyrics))
    data = response_formatter.format_advice_response(raw)

    return {
        "title": "Life Advice",
        "content": data.advice,
        "meta": {}
    }


life_advice = lyric_advice
