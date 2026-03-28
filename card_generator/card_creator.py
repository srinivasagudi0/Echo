def generate_card(result):
    return {
        "title": result["title"],
        "content": result["content"],
        "meta": result.get("meta", {})
    }