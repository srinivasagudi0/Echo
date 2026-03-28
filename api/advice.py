from fastapi import APIRouter

from engine.mode_router import route_mode
from models.song import CardResponse, LyricsRequest


router = APIRouter()


@router.post("/advice", response_model=CardResponse)
async def advice(payload: LyricsRequest) -> CardResponse:
    return CardResponse.model_validate(route_mode("advice", payload.model_dump()))
