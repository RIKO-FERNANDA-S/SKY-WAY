# app/db/models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class WaypointModel(SQLModel, table=True):
    __tablename__ = "waypoints"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    waypoint_id: int = Field(index=True)
    mission_id: str = Field(foreign_key="missions.id", index=True)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    altitude: float = Field(..., ge=0)  # Pastikan ejaannya 'altitude'
    speed: Optional[float] = Field(default=10.0, ge=0)
    hold_time: Optional[int] = Field(default=0, ge=0)
    
    mission: "MissionModel" = Relationship(back_populates="waypoints")

class MissionModel(SQLModel, table=True):
    __tablename__ = "missions"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8], primary_key=True, index=True)
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    status: str = Field(default="PENDING", index=True)
    current_waypoint: Optional[int] = Field(default=None)
    created_at: float = Field(default_factory=lambda: datetime.now().timestamp())
    updated_at: Optional[float] = Field(default=None)
    
    # PERBAIKAN DI SINI: Tambahkan "lazy": "selectin"
    waypoints: List["WaypointModel"] = Relationship(
        back_populates="mission", 
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"  # <-- Ini memaksa load async yang aman
        }
    )