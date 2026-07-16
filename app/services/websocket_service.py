# app/services/websocket_service.py
from app.websocket.manager import manager
import logging

logger = logging.getLogger(__name__)

class WebSocketService:
    """
    Wrapper untuk WebSocket manager dengan metode yang lebih tinggi
    """
    
    async def broadcast(self, message: dict):
        """Broadcast message ke semua connected clients"""
        await manager.broadcast(message)
    
    async def send_telemetry(self, telemetry_data: dict):
        """Kirim data telemetry"""
        await self.broadcast({
            "type": "telemetry",
            "data": telemetry_data
        })
    
    async def send_mission_update(self, mission_id: str, status: str, message: str):
        """Kirim update status misi"""
        await self.broadcast({
            "type": "mission_update",
            "data": {
                "mission_id": mission_id,
                "status": status,
                "message": message
            }
        })

# Singleton instance
websocket_service = WebSocketService()