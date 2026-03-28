from fastapi import APIRouter

from engine.ai_client import is_ai_configured
from models.song import HealthResponse


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(ai_configured=is_ai_configured())
