from fastapi import APIRouter

from engine.mode_router import route_mode
from models.song import CardResponse, CompareRequest


router = APIRouter()


@router.post("/compare", response_model=CardResponse)
async def compare(payload: CompareRequest) -> CardResponse:
    return CardResponse.model_validate(route_mode("compare", payload.model_dump()))
