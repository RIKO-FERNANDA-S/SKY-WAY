from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["WebSocket"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received message from client: {data}")

            await manager.send_personal_message({
                "type": "ack",
                "message": f"Server received: {data}"
            }, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)