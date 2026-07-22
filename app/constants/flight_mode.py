from enum import Enum 

class FlightMode(str, Enum):
    Manual = "MANUAL"
    STABILIZE = "STABILIZE"
    AUTO = "AUTO"
    RTL = "RTL"
    HOLD = "HOLD"
    LAND = "LAND"