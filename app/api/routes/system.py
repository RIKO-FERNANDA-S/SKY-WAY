# app/api/routes/system.py
from fastapi import APIRouter
from app.schemas.response import APIResponse
from app.services.system_service import system_service

router = APIRouter(prefix="/system", tags=["System"])

@router.get("/", response_model=APIResponse)
async def get_system_status():
    """Get comprehensive system status"""
    status = system_service.get_full_system_status()
    return APIResponse(
        success=True,
        message="System status retrieved successfully",
        data=status
    )

@router.get("/cpu", response_model=APIResponse)
async def get_cpu_status():
    """Get CPU status"""
    return APIResponse(
        success=True,
        message="CPU status retrieved successfully",
        data=system_service.get_cpu_info()
    )

@router.get("/memory", response_model=APIResponse)
async def get_memory_status():
    """Get memory status"""
    return APIResponse(
        success=True,
        message="Memory status retrieved successfully",
        data=system_service.get_memory_info()
    )

@router.get("/disk", response_model=APIResponse)
async def get_disk_status():
    """Get disk status"""
    return APIResponse(
        success=True,
        message="Disk status retrieved successfully",
        data=system_service.get_disk_info()
    )

@router.get("/temperature", response_model=APIResponse)
async def get_temperature_status():
    """Get temperature status"""
    return APIResponse(
        success=True,
        message="Temperature status retrieved successfully",
        data=system_service.get_temperature()
    )