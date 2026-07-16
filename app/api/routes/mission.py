# app/api/routes/mission.py
from fastapi import APIRouter, HTTPException
from app.schemas.response import APIResponse
from app.schemas.mission import MissionCreate, MissionResponse
from app.services.mission_service import mission_service
from typing import List

router = APIRouter(prefix="/mission", tags=["Mission"])

@router.post("/", response_model=APIResponse, status_code=201)
async def create_mission(mission_data: MissionCreate):
    """Create new mission"""
    try:
        mission = mission_service.create_mission(mission_data)
        return APIResponse(
            success=True,
            message="Mission created successfully",
            data=mission.dict()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=APIResponse)
async def get_all_missions():
    """Get all missions"""
    missions = mission_service.get_all_missions()
    return APIResponse(
        success=True,
        message="Missions retrieved successfully",
        data=[m.dict() for m in missions]
    )

@router.get("/{mission_id}", response_model=APIResponse)
async def get_mission(mission_id: str):
    """Get specific mission by ID"""
    mission = mission_service.get_mission(mission_id)
    if not mission:
        return APIResponse(
            success=False,
            message="Mission not found",
            data=None
        )
    
    return APIResponse(
        success=True,
        message="Mission retrieved successfully",
        data=mission.dict()
    )

@router.delete("/{mission_id}", response_model=APIResponse)
async def delete_mission(mission_id: str):
    """Delete mission"""
    success = mission_service.delete_mission(mission_id)
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
async def start_mission(mission_id: str):
    """Start mission execution"""
    success = await mission_service.start_mission(mission_id)
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
async def abort_mission(mission_id: str):
    """Abort running mission"""
    success = await mission_service.abort_mission(mission_id)
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