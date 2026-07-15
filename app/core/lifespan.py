# app/core/lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
import asyncio

# Import simulator secara spesifik
from app.telemetry.simulator import TelemetrySimulator

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    logger.info("🚀 Starting VTOL Drone Backend...")
    
    # Buat instance simulator di sini agar scope-nya jelas
    telemetry_sim = TelemetrySimulator()
    
    # Jalankan simulator sebagai background task
    # Kita simpan task-nya agar bisa di-cancel saat shutdown jika perlu
    sim_task = asyncio.create_task(telemetry_sim.start())
    
    logger.info("✅ Telemetry Simulator is running in the background")
    
    yield
    
    # --- SHUTDOWN ---
    logger.info("🛑 Shutting down VTOL Drone Backend...")
    
    # Hentikan simulator
    await telemetry_sim.stop()
    
    # Pastikan task selesai
    if not sim_task.done():
        sim_task.cancel()
        try:
            await sim_task
        except asyncio.CancelledError:
            pass
            
    logger.info("✅ Cleanup finished")