# Echo

Echo is a local Streamlit app backed by shared Python lyric-processing logic. It supports five modes:

- `analyze` for meaning, emotion, theme, and key lines
- `compare` for emotional contrast between two lyric excerpts
- `remix` for a motivational rewrite
- `advice` for practical life guidance
- `story` for a cinematic retelling

## Requirements

- Python 3.11+
- An OpenAI API key

## Setup

1. Create a virtual environment.
2. Install dependencies.
3. Copy `.env.example` to `.env` and fill in your values.
4. Start the Streamlit UI.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run streamlit_app.py
```

The UI will be available at `http://localhost:8501`.

## Environment Variables

- `OPENAI_API_KEY`: required for all lyric-processing endpoints
- `OPENAI_MODEL`: required model name, for example `gpt-4o-mini`
- `OPENAI_BASE_URL`: optional override for compatible gateways
- `OPENAI_TIMEOUT`: optional request timeout in seconds, default `30`
- `MAX_LYRICS_LENGTH`: optional input cap, default `5000`

## Running the API

The FastAPI app still exists for programmatic use and tests:

```bash
uvicorn main:app --reload
```

## API Routes

- `GET /api/health`
- `POST /api/analyze`
- `POST /api/compare`
- `POST /api/remix`
- `POST /api/advice`
- `POST /api/story`

Request bodies:

- Single-input modes use `{"lyrics": "..."}`.
- Compare mode uses `{"lyrics_a": "...", "lyrics_b": "..."}`.

Every mode returns:

```json
{
  "title": "string",
  "content": "string",
  "meta": {}
}
```

## Testing

Run the automated checks with:

```bash
pytest
```

## Manual Streamlit Checklist

- Start the UI with `streamlit run streamlit_app.py`.
- Switch through all five modes and confirm the hero copy updates.
- Submit valid lyric text in each mode and confirm a result card appears.
- Submit blank input and confirm a visible validation error appears.
- Use compare mode with two lyric excerpts and confirm both text areas are required.
- Confirm the sidebar status reflects whether OpenAI is configured.
