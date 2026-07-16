# app/db/config.py
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os

# Database URL - menggunakan SQLite
DATABASE_URL = "sqlite+aiosqlite:///./data/vtol.db"

# Create async engine untuk SQLite
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set True untuk debug SQL queries
    future=True
)

# Async session factory
async_session_maker = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency untuk mendapatkan database session.
    Digunakan di FastAPI routes.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """
    Initialize database - buat semua tabel
    Dipanggil saat aplikasi startup
    """
    async with engine.begin() as conn:
        # Import semua models di sini untuk memastikan mereka terdaftar
        from app.db.models import MissionModel, WaypointModel  # noqa
        
        await conn.run_sync(SQLModel.metadata.create_all)