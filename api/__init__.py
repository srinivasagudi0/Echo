from fastapi import APIRouter

from api.advice import router as advice_router
from api.analyze import router as analyze_router
from api.compare import router as compare_router
from api.health import router as health_router
from api.remix import router as remix_router
from api.story import router as story_router


api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(analyze_router)
api_router.include_router(compare_router)
api_router.include_router(remix_router)
api_router.include_router(advice_router)
api_router.include_router(story_router)
