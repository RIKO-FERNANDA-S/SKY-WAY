# app/api/routes/mission.py
from fastapi import APIRouter, Depends, HTTPException, logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.response import APIResponse
from app.schemas.mission import MissionCreate
from app.services.mission_service import mission_service
from app.db.config import get_db
from typing import List
from app.constants.flight_mode import FlightMode
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mission", tags=["Mission"])

@router.post("/", response_model=APIResponse, status_code=201)
async def create_mission(
    mission_data: MissionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new mission"""
    try:
        mission = await mission_service.create_mission(db, mission_data)
        return APIResponse(
            success=True,
            message="Mission created successfully",
            data=mission
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=APIResponse)
async def get_all_missions(db: AsyncSession = Depends(get_db)):
    """Get all missions"""
    missions = await mission_service.get_all_missions(db)
    return APIResponse(
        success=True,
        message="Missions retrieved successfully",
        data=missions
    )

@router.get("/{mission_id}", response_model=APIResponse)
async def get_mission(mission_id: str, db: AsyncSession = Depends(get_db)):
    """Get specific mission by ID"""
    mission = await mission_service.get_mission(db, mission_id)
    
    if not mission:
        return APIResponse(
            success=False,
            message="Mission not found",
            data=None
        )
    
    return APIResponse(
        success=True,
        message="Mission retrieved successfully",
        data=mission
    )

@router.delete("/{mission_id}", response_model=APIResponse)
async def delete_mission(mission_id: str, db: AsyncSession = Depends(get_db)):
    """Delete mission"""
    success = await mission_service.delete_mission(db, mission_id)
    
    if not success:
        return APIResponse(
            success=False,
            message="Mission not found",
            data=None
        )
    
    return APIResponse(
        success=True,
        message="Mission deleted successfully",
        data=None
    )

@router.post("/{mission_id}/start", response_model=APIResponse)
async def start_mission(mission_id: str, db: AsyncSession = Depends(get_db)):
    """Start mission execution"""
    success = await mission_service.start_mission(db, mission_id)
    
    if not success:
        return APIResponse(
            success=False,
            message="Failed to start mission",
            data=None
        )
    
    return APIResponse(
        success=True,
        message="Mission started successfully",
        data={"mission_id": mission_id}
    )

@router.post("/{mission_id}/abort", response_model=APIResponse)
async def abort_mission(mission_id: str, db: AsyncSession = Depends(get_db)):
    """Abort running mission"""
    success = await mission_service.abort_mission(db, mission_id)
    
    if not success:
        return APIResponse(
            success=False,
            message="Failed to abort mission",
            data=None
        )
    
    return APIResponse(
        success=True,
        message="Mission aborted successfully",
        data={"mission_id": mission_id}
    )


@router.post("/mode", response_model=APIResponse)
async def change_flight_mode(mode: FlightMode):
    """
    Software override untuk mengganti flight mode. 
    Nantinya di sprint 6, ini akan mengirim MAVLink command SET_MODE ke Pixhwak.
    """
    logger.info(f"🕹️ Software override: Requesting mode change to {mode.value}")

    return APIResponse(
        success=True,
        message=f"Mode change Request: {mode.value}",
        data={"request_mode": mode.value}
    )