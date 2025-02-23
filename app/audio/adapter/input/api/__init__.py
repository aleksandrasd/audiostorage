from fastapi import APIRouter

from app.audio.adapter.input.api.v1.audio import router as audio_v1_router

router = APIRouter()
router.include_router(audio_v1_router, prefix="", tags=["Audio"])


__all__ = ["router"]
