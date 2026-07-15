# app/core/lifespan.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting VTOL Drone Backend...")
    logger.info(f"✅ App Name: {app.title}")
    logger.info(f"✅ Version: {app.version}")
    
    # Di sini nanti kita bisa start background tasks seperti telemetry simulator
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down VTOL Drone Backend...")
    # Di sini kita bisa stop background tasks atau close connections