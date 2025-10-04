"""
Configuration module for Exoplanet Explorer API
"""
import os
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_host: str = "localhost"
    api_port: int = 8000
    debug: bool = True
    
    # External APIs
    nasa_exoplanet_api_url: str = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    mast_api_url: str = "https://mast.stsci.edu/api/v0.1"
    
    # CORS Settings
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # Cache Settings
    cache_ttl_seconds: int = 3600
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()