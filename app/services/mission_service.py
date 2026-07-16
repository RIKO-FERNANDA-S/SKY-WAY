# app/services/mission_service.py
from typing import Dict, Optional, List
from app.schemas.mission import MissionCreate, MissionResponse, MissionStatus, Waypoint
from app.services.websocket_service import websocket_service
import asyncio
import time
import uuid
import logging

logger = logging.getLogger(__name__)

class MissionService:
    def __init__(self):
        self.missions: Dict[str, MissionResponse] = {}
        self.current_mission_id: Optional[str] = None
        self.is_executing = False

    def create_mission(self, mission_data: MissionCreate) -> MissionResponse:
        mission_id = str(uuid.uuid4())[:8]
        timestamp = time.time()
        
        mission = MissionResponse(
            id=mission_id,
            name=mission_data.name,
            description=mission_data.description,
            waypoints=mission_data.waypoints,
            status=MissionStatus.PENDING,
            current_waypoint=None,
            created_at=timestamp,
            updated_at=timestamp
        )
        
        self.missions[mission_id] = mission
        logger.info(f"✅ Mission created: {mission_id} - {mission.name}")
        
        return mission

    def get_mission(self, mission_id: str) -> Optional[MissionResponse]:
        return self.missions.get(mission_id)

    def get_all_missions(self) -> List[MissionResponse]:
        return list(self.missions.values())

    def delete_mission(self, mission_id: str) -> bool:
        if mission_id in self.missions:
            del self.missions[mission_id]
            logger.info(f"️ Mission deleted: {mission_id}")
            return True
        return False

    async def start_mission(self, mission_id: str) -> bool:
        mission = self.get_mission(mission_id)
        if not mission:
            return False
        
        if mission.status != MissionStatus.PENDING:
            logger.warning(f"Mission {mission_id} cannot be started (status: {mission.status})")
            return False
        
        self.current_mission_id = mission_id
        mission.status = MissionStatus.RUNNING
        mission.updated_at = time.time()
        self.is_executing = True
        
        logger.info(f"🚀 Starting mission: {mission_id}")
        
        # Start mission executor in background
        asyncio.create_task(self._execute_mission(mission_id))
        
        return True

    async def abort_mission(self, mission_id: str) -> bool:
        mission = self.get_mission(mission_id)
        if not mission or mission.status != MissionStatus.RUNNING:
            return False
        
        mission.status = MissionStatus.ABORTED
        mission.updated_at = time.time()
        self.is_executing = False
        self.current_mission_id = None
        
        logger.info(f"🛑 Mission aborted: {mission_id}")
        
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

    async def _execute_mission(self, mission_id: str):
        """
        Mission executor - simulasi eksekusi waypoint
        Di Sprint 5, ini akan diganti dengan MAVLink commands
        """
        mission = self.get_mission(mission_id)
        if not mission:
            return
        
        try:
            for i, waypoint in enumerate(mission.waypoints):
                if not self.is_executing:
                    break
                
                mission.current_waypoint = waypoint.id
                mission.updated_at = time.time()
                
                logger.info(f"📍 Executing waypoint {i+1}/{len(mission.waypoints)}: {waypoint.latitude}, {waypoint.longitude}")
                
                # Broadcast waypoint update
                await websocket_service.broadcast({
                    "type": "waypoint_update",
                    "data": {
                        "mission_id": mission_id,
                        "current_waypoint": waypoint.id,
                        "total_waypoints": len(mission.waypoints),
                        "latitude": waypoint.latitude,
                        "longitude": waypoint.longitude,
                        "altitude": waypoint.altitude
                    }
                })
                
                # Simulasi waktu tempuh ke waypoint
                await asyncio.sleep(3)  # 3 detik per waypoint (simulasi)
            
            if self.is_executing:
                mission.status = MissionStatus.COMPLETED
                mission.updated_at = time.time()
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
            mission.status = MissionStatus.FAILED
            mission.updated_at = time.time()
        
        finally:
            self.is_executing = False
            self.current_mission_id = None

# Singleton instance
mission_service = MissionService()