# app/telemetry/simulator.py
import asyncio
import random
import time
from app.websocket.manager import manager
import logging

logger = logging.getLogger(__name__)

class TelemetrySimulator:
    def __init__(self):
        self.is_running = False
        self.battery_level = 100.0
        self.altitude = 0.0
        self.latitude = -6.200000
        self.longitude = 106.816666

    async def start(self):
        self.is_running = True
        logger.info("🛰️ Telemetry Simulator started")
        while self.is_running:
            await self._generate_telemetry()
            await asyncio.sleep(1) # Update setiap 1 detik

    async def stop(self):
        self.is_running = False
        logger.info("🛑 Telemetry Simulator stopped")

    async def _generate_telemetry(self):
        """
        Menghasilkan data dummy yang realistis.
        """
        # Simulasi perubahan battery
        if self.battery_level > 0:
            self.battery_level -= random.uniform(0.01, 0.05)
        
        # Simulasi gerakan drone (naik turun sedikit)
        self.altitude += random.uniform(-0.5, 0.5)
        if self.altitude < 0: self.altitude = 0

        # Simulasi pergerakan GPS
        self.latitude += random.uniform(-0.00001, 0.00001)
        self.longitude += random.uniform(-0.00001, 0.00001)

        telemetry_data = {
            "type": "telemetry",
            "timestamp": time.time(),
            "data": {
                "battery": round(self.battery_level, 2),
                "altitude": round(self.altitude, 2),
                "latitude": round(self.latitude, 6),
                "longitude": round(self.longitude, 6),
                "speed": round(random.uniform(0, 15), 2),
                "heading": round(random.uniform(0, 360), 2),
                "status": "ARMED" if self.altitude > 0 else "DISARMED"
            }
        }

        # Kirim ke semua frontend yang terhubung
        await manager.broadcast(telemetry_data)