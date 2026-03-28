from engine import ai_client, prompt_builder, response_formatter

def remix_meaning(lyrics):
    raw = ai_client.call_ai(prompt_builder.build_remix_prompt(lyrics))
    data = response_formatter.format_remix_response(raw)

    return {
        "title": "Remix Meaning",
        "content": data.remix,
        "meta": {}
    }
