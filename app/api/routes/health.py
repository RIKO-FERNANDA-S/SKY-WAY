# app/api/routes/health.py
from fastapi import APIRouter
from app.schemas.response import APIResponse
from app.core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=APIResponse)
def health_check():
    return APIResponse(
        success=True,
        message="System is healthy",
        data={
            "status": "online",
            "version": settings.app_version
        }
    )