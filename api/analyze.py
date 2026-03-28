from fastapi import APIRouter

from engine.mode_router import route_mode
from models.song import CardResponse, LyricsRequest


router = APIRouter()


@router.post("/analyze", response_model=CardResponse)
async def analyze(payload: LyricsRequest) -> CardResponse:
    return CardResponse.model_validate(route_mode("analyze", payload.model_dump()))
