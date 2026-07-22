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
        
        # Home position (Jetson location)
        self.home_lat = -6.200000
        self.home_lon = 106.816666
        
        self.latitude = self.home_lat
        self.longitude = self.home_lon
        self.altitude = 0.0
        self.battery_level = 100.0
        
        # Flight Profile State Machine
        self.flight_state = "DISARMED" 
        self.target_altitude = 30.0 # meter
        self.target_lat = self.home_lat + 0.001  # Dummy waypoint ~100m away
        self.target_lon = self.home_lon + 0.001

    async def start(self):
        self.is_running = True
        logger.info("🛰️ Flight Profile Simulator started")
        
        # Jalankan profil penerbangan otomatis
        await self._run_flight_profile()
        
        self.is_running = False
        logger.info("✅ Flight Profile completed. Simulator stopped to save CPU.")

    async def stop(self):
        self.is_running = False
        logger.info("🛑 Simulator forcefully stopped")

    async def _run_flight_profile(self):
        """Simulasi satu siklus penerbangan lengkap, lalu berhenti."""
        
        # 1. DISARMED (Idle selama 3 detik)
        self.flight_state = "DISARMED"
        await self._broadcast_telemetry(FlightMode.MANUAL)
        await asyncio.sleep(3)

        # 2. TAKING OFF
        logger.info("🚀 Simulating TAKEOFF...")
        self.flight_state = "TAKING_OFF"
        while self.altitude < self.target_altitude and self.is_running:
            self.altitude += 1.0
            self.battery_level -= 0.1
            await self._broadcast_telemetry(FlightMode.AUTO)
            await asyncio.sleep(0.5) # Naik 2m/detik

        # 3. MISSION (Terbang ke waypoint dummy)
        logger.info("📍 Simulating MISSION execution...")
        self.flight_state = "MISSION"
        steps = 20
        for _ in range(steps):
            if not self.is_running: break
            # Gerak mendekati target
            self.latitude += (self.target_lat - self.latitude) / steps
            self.longitude += (self.target_lon - self.longitude) / steps
            self.battery_level -= 0.2
            await self._broadcast_telemetry(FlightMode.AUTO)
            await asyncio.sleep(0.5)

        # 4. RTL (Return to Launch)
        logger.info("🔄 Simulating RTL (Return to Launch)...")
        self.flight_state = "RTL"
        for _ in range(steps):
            if not self.is_running: break
            # Gerak kembali ke home
            self.latitude += (self.home_lat - self.latitude) / steps
            self.longitude += (self.home_lon - self.longitude) / steps
            self.battery_level -= 0.2
            await self._broadcast_telemetry(FlightMode.RTL)
            await asyncio.sleep(0.5)

        # 5. LANDING
        logger.info("🛬 Simulating LANDING...")
        self.flight_state = "LANDING"
        while self.altitude > 0 and self.is_running:
            self.altitude -= 1.0
            self.battery_level -= 0.1
            await self._broadcast_telemetry(FlightMode.LAND)
            await asyncio.sleep(0.5)

        # 6. KEMBALI KE DISARMED & BERHENTI
        self.altitude = 0.0
        self.latitude = self.home_lat
        self.longitude = self.home_lon
        self.flight_state = "DISARMED"
        await self._broadcast_telemetry(FlightMode.MANUAL)
        logger.info("🏁 Drone landed and disarmed. Simulator shutting down.")

    async def _broadcast_telemetry(self, current_mode: FlightMode):
        """Helper untuk mengirim data ke WebSocket"""
        telemetry = TelemetryData(
            battery=round(max(0, self.battery_level), 2),
            altitude=round(max(0, self.altitude), 2),
            latitude=round(self.latitude, 6),
            longitude=round(self.longitude, 6),
            speed=round(5.0 if self.flight_state in ["MISSION", "RTL"] else 0.0, 2),
            heading=round(random.uniform(0, 360), 2),
            status="ARMED" if self.altitude > 0 else "DISARMED",
            flight_mode=current_mode
        )

        await manager.broadcast({
            "type": "telemetry",
            "timestamp": time.time(),
            "data": telemetry.dict()
        })