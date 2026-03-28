from engine import ai_client, prompt_builder, response_formatter

def story_mode(lyrics):
    raw = ai_client.call_ai(prompt_builder.build_story_prompt(lyrics))
    data = response_formatter.format_story_response(raw)

    return {
        "title": "Story Mode",
        "content": data.story,
        "meta": {}
    }
