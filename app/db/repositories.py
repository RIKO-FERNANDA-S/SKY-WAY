# app/db/repositories.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload  # <-- IMPORT INI
from typing import Optional, List
from app.db.models import MissionModel, WaypointModel
from app.schemas.mission import MissionStatus
import logging

logger = logging.getLogger(__name__)

class MissionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, mission: MissionModel, waypoints: List[WaypointModel]) -> MissionModel:
        self.session.add(mission)
        for wp in waypoints:
            self.session.add(wp)
        await self.session.commit()
        await self.session.refresh(mission)
        logger.info(f"✅ Mission created in DB: {mission.id}")
        return mission
    
    async def get_by_id(self, mission_id: str) -> Optional[MissionModel]:
        # PERBAIKAN: Gunakan selectinload untuk mengambil waypoints sekaligus
        stmt = (
            select(MissionModel)
            .options(selectinload(MissionModel.waypoints))
            .where(MissionModel.id == mission_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self) -> List[MissionModel]:
        # PERBAIKAN: Gunakan selectinload di sini juga
        stmt = select(MissionModel).options(selectinload(MissionModel.waypoints))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def update(self, mission: MissionModel) -> MissionModel:
        from datetime import datetime
        mission.updated_at = datetime.now().timestamp()
        await self.session.commit()
        await self.session.refresh(mission)
        logger.info(f"✏️ Mission updated: {mission.id}")
        return mission
    
    async def delete(self, mission_id: str) -> bool:
        # Hapus waypoints dulu (meski cascade seharusnya menangani, ini lebih aman)
        await self.session.execute(
            delete(WaypointModel).where(WaypointModel.mission_id == mission_id)
        )
        
        result = await self.session.execute(
            delete(MissionModel).where(MissionModel.id == mission_id)
        )
        await self.session.commit()
        
        if result.rowcount > 0:
            logger.info(f"🗑️ Mission deleted: {mission_id}")
            return True
        return False
    
    async def update_status(self, mission_id: str, status: MissionStatus, current_waypoint: Optional[int] = None) -> Optional[MissionModel]:
        mission = await self.get_by_id(mission_id)
        if mission:
            mission.status = status.value
            mission.current_waypoint = current_waypoint
            await self.update(mission)
        return mission