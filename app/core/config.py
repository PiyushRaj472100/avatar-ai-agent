"""
Configuration and environment settings for Avatar AI Agent
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    
    # LLM Configuration
    gemini_api_key: str = ""
    model_name: str = "gemini-pro"
    max_tokens: int = 1000
    temperature: float = 0.7
    
    # Memory Configuration
    memory_file_path: str = "app/memory/memory.json"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
