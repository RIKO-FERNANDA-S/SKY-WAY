from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "VtOL Backend"
    app_version: str = "0.1.0"

    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    log_level: str = "INFO"

    cors_origins: List[str] = ["http://localhost:3000"]

    class Config: 
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_setting() -> Settings:
    """
    Mek digae peng pisan coy 
    """
    return Settings()

settings = get_setting()