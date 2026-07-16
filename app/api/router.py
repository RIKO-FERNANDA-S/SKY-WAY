# app/api/router.py
from fastapi import APIRouter
from app.api.routes.health import router as health_router
from app.api.routes.websocket import router as websocket_router
from app.api.routes.mission import router as mission_router
from app.api.routes.system import router as system_router

# Import router lain nantinya

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(websocket_router)
api_router.include_router(mission_router)
api_router.include_router(system_router)