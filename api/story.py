from fastapi import APIRouter

from engine.mode_router import route_mode
from models.song import CardResponse, LyricsRequest


router = APIRouter()


@router.post("/story", response_model=CardResponse)
async def story(payload: LyricsRequest) -> CardResponse:
    return CardResponse.model_validate(route_mode("story", payload.model_dump()))
