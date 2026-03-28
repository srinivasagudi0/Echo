from modes.lyric_converter import analyze_lyrics
from modes.song_compare import compare_songs
from modes.remix_meaning import remix_meaning
from modes.life_advice import lyric_advice
from modes.story_mode import story_mode
from utils.helpers import InvalidModeError


MODE_HANDLERS = {
    "analyze": lambda payload: analyze_lyrics(payload["lyrics"]),
    "compare": lambda payload: compare_songs(payload["lyrics_a"], payload["lyrics_b"]),
    "remix": lambda payload: remix_meaning(payload["lyrics"]),
    "advice": lambda payload: lyric_advice(payload["lyrics"]),
    "story": lambda payload: story_mode(payload["lyrics"]),
}


def route_mode(mode, data):
    handler = MODE_HANDLERS.get(mode)
    if handler is None:
        raise InvalidModeError(mode)
    return handler(data)
