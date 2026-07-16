# app/core/lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
import asyncio
from app.telemetry.simulator import TelemetrySimulator
from app.db.config import init_db

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    logger.info(" Starting VTOL Drone Backend...")
    
    # Initialize database
    logger.info("️ Initializing database...")
    await init_db()
    logger.info("✅ Database initialized")
    
    # Start telemetry simulator
    telemetry_sim = TelemetrySimulator()
    sim_task = asyncio.create_task(telemetry_sim.start())
    
    logger.info("✅ Telemetry Simulator is running in the background")
    
    yield
    
    # --- SHUTDOWN ---
    logger.info("🛑 Shutting down VTOL Drone Backend...")
    
    # Stop simulator
    await telemetry_sim.stop()
    
    if not sim_task.done():
        sim_task.cancel()
        try:
            await sim_task
        except asyncio.CancelledError:
            pass
    
    logger.info("✅ Cleanup finished")