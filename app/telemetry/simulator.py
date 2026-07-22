# app/telemetry/simulator.py
import asyncio
import random
import time
from app.websocket.manager import manager
from app.schemas.telemetry import TelemetryData
from app.constants.flight_mode import FlightMode
import logging

logger = logging.getLogger(__name__)

class TelemetrySimulator:
    def __init__(self):
        self.is_running = False
        self.battery_level = 100.0
        self.altitude = 0.0
        self.latitude = -6.200000
        self.longitude = 106.816666
        self.current_mode = FlightMode.STABILIZE
        self.mode_switch_counter = 0

    async def start(self):
        self.is_running = True
        logger.info("🛰️ Telemetry Simulator started")
        while self.is_running:
            await self._generate_telemetry()
            await asyncio.sleep(1)

    async def stop(self):
        self.is_running = False
        logger.info("🛑 Telemetry Simulator stopped")

    async def _generate_telemetry(self):
        # Simulasi perubahan battery
        if self.battery_level > 0:
            self.battery_level -= random.uniform(0.01, 0.05)
        
        # Simulasi gerakan drone
        self.altitude += random.uniform(-0.5, 0.5)
        if self.altitude < 0: self.altitude = 0

        self.latitude += random.uniform(-0.00001, 0.00001)
        self.longitude += random.uniform(-0.00001, 0.00001)

        # --- SIMULASI PERUBAHAN MODE VIA RC ---
        self.mode_switch_counter += 1
        if self.mode_switch_counter % 15 == 0:  # Setiap 15 detik
            if self.current_mode == FlightMode.AUTO:
                self.current_mode = FlightMode.STABILIZE
                logger.info("📡 [SIMULASI RC] Switching to MANUAL/STABILIZE mode")
            else:
                self.current_mode = FlightMode.AUTO
                logger.info("📡 [SIMULASI RC] Switching to AUTO mode")

        telemetry = TelemetryData(
            battery=round(self.battery_level, 2),
            altitude=round(self.altitude, 2),
            latitude=round(self.latitude, 6),
            longitude=round(self.longitude, 6),
            speed=round(random.uniform(0, 15), 2),
            heading=round(random.uniform(0, 360), 2),
            status="ARMED" if self.altitude > 0 else "DISARMED",
            flight_mode=self.current_mode
        )

        await manager.broadcast({
            "type": "telemetry",
            "timestamp": time.time(),
            "data": telemetry.dict()
        })