# app/services/mission_service.py
from typing import Dict, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.mission import MissionCreate, MissionStatus, Waypoint
from app.db.models import MissionModel, WaypointModel
from app.db.repositories import MissionRepository
from app.services.websocket_service import websocket_service
import asyncio
import time
import logging

logger = logging.getLogger(__name__)

class MissionService:
    def __init__(self):
        self.is_executing = False
        self.current_mission_id: Optional[str] = None

    def _convert_to_schema(self, mission: MissionModel) -> dict:
        """Convert database model to schema dict"""
        return {
            "id": mission.id,
            "name": mission.name,
            "description": mission.description,
            "waypoints": [
                {
                    "id": wp.waypoint_id,
                    "latitude": wp.latitude,
                    "longitude": wp.longitude,
                    "altitude": wp.altitude,
                    "speed": wp.speed,
                    "hold_time": wp.hold_time
                }
                for wp in mission.waypoints
            ],
            "status": mission.status,
            "current_waypoint": mission.current_waypoint,
            "created_at": mission.created_at,
            "updated_at": mission.updated_at
        }

    async def create_mission(self, db: AsyncSession, mission_data: MissionCreate) -> dict:
        """Create new mission in database"""
        repo = MissionRepository(db)
        
        # Create mission model
        mission = MissionModel(
            name=mission_data.name,
            description=mission_data.description,
            status=MissionStatus.PENDING.value
        )
        
        # Create waypoint models
        waypoints = [
            WaypointModel(
                waypoint_id=wp.id,
                mission_id=mission.id,  # Will be set after mission is added
                latitude=wp.latitude,
                longitude=wp.longitude,
                altitude=wp.altitude,
                speed=wp.speed,
                hold_time=wp.hold_time
            )
            for wp in mission_data.waypoints
        ]
        
        # Save to database
        saved_mission = await repo.create(mission, waypoints)
        
        logger.info(f"✅ Mission created: {saved_mission.id} - {saved_mission.name}")
        
        return self._convert_to_schema(saved_mission)

    async def get_mission(self, db: AsyncSession, mission_id: str) -> Optional[dict]:
        """Get mission by ID"""
        repo = MissionRepository(db)
        mission = await repo.get_by_id(mission_id)
        
        if mission:
            return self._convert_to_schema(mission)
        return None

    async def get_all_missions(self, db: AsyncSession) -> List[dict]:
        """Get all missions"""
        repo = MissionRepository(db)
        missions = await repo.get_all()
        
        return [self._convert_to_schema(m) for m in missions]

    async def delete_mission(self, db: AsyncSession, mission_id: str) -> bool:
        """Delete mission"""
        repo = MissionRepository(db)
        return await repo.delete(mission_id)

    async def start_mission(self, db: AsyncSession, mission_id: str) -> bool:
        """Start mission execution"""
        repo = MissionRepository(db)
        mission = await repo.get_by_id(mission_id)
        
        if not mission:
            return False
        
        if mission.status != MissionStatus.PENDING.value:
            logger.warning(f"Mission {mission_id} cannot be started (status: {mission.status})")
            return False
        
        # Update status to RUNNING
        await repo.update_status(mission_id, MissionStatus.RUNNING)
        
        self.current_mission_id = mission_id
        self.is_executing = True
        
        logger.info(f"🚀 Starting mission: {mission_id}")
        
        # Start mission executor in background
        asyncio.create_task(self._execute_mission(db, mission_id))
        
        return True

    async def abort_mission(self, db: AsyncSession, mission_id: str) -> bool:
        """Abort running mission"""
        repo = MissionRepository(db)
        mission = await repo.get_by_id(mission_id)
        
        if not mission or mission.status != MissionStatus.RUNNING.value:
            return False
        
        # Update status
        await repo.update_status(mission_id, MissionStatus.ABORTED)
        
        self.is_executing = False
        self.current_mission_id = None
        
        logger.info(f" Mission aborted: {mission_id}")
        
        # Broadcast status
        await websocket_service.broadcast({
            "type": "mission_update",
            "data": {
                "mission_id": mission_id,
                "status": "ABORTED",
                "message": "Mission aborted by user"
            }
        })
        
        return True

    async def _execute_mission(self, db: AsyncSession, mission_id: str):
        """
        Mission executor - simulasi eksekusi waypoint
        """
        repo = MissionRepository(db)
        mission = await repo.get_by_id(mission_id)
        
        if not mission:
            return
        
        try:
            for i, wp in enumerate(mission.waypoints):
                if not self.is_executing:
                    break
                
                # Update current waypoint
                await repo.update_status(
                    mission_id, 
                    MissionStatus.RUNNING,
                    current_waypoint=wp.waypoint_id
                )
                
                logger.info(f"📍 Executing waypoint {i+1}/{len(mission.waypoints)}: {wp.latitude}, {wp.longitude}")
                
                # Broadcast waypoint update
                await websocket_service.broadcast({
                    "type": "waypoint_update",
                    "data": {
                        "mission_id": mission_id,
                        "current_waypoint": wp.waypoint_id,
                        "total_waypoints": len(mission.waypoints),
                        "latitude": wp.latitude,
                        "longitude": wp.longitude,
                        "altitude": wp.altitude
                    }
                })
                
                # Simulasi waktu tempuh
                await asyncio.sleep(3)
            
            if self.is_executing:
                await repo.update_status(mission_id, MissionStatus.COMPLETED)
                logger.info(f"✅ Mission completed: {mission_id}")
                
                await websocket_service.broadcast({
                    "type": "mission_update",
                    "data": {
                        "mission_id": mission_id,
                        "status": "COMPLETED",
                        "message": "Mission completed successfully"
                    }
                })
        
        except Exception as e:
            logger.error(f"❌ Mission failed: {e}")
            await repo.update_status(mission_id, MissionStatus.FAILED)
        
        finally:
            self.is_executing = False
            self.current_mission_id = None

# Singleton instance
mission_service = MissionService()