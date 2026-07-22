from pydantic import BaseModel
from app.constants.flight_mode import FlightMode

class TelemetryData(BaseModel):
    battery: float
    altitude: float
    latitude: float
    longtitude: float
    speed: float
    heading: float
    status: str
    flight_mode: FlightMode = FlightMode.STABILIZE