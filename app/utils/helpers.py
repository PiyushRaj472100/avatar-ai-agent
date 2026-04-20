"""
Helper utilities for Avatar AI Agent
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict

def setup_logging(log_level: str = "INFO"):
    """
    Setup logging configuration
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('avatar_agent.log'),
            logging.StreamHandler()
        ]
    )

def format_timestamp(timestamp: str) -> str:
    """
    Format timestamp for display
    """
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return timestamp

def sanitize_command(command: str) -> str:
    """
    Sanitize user command for safety
    """
    # Remove potentially dangerous characters
    dangerous_chars = [';', '|', '&', '`', '$', '(', ')', '{', '}', '[', ']', '<', '>', '"', "'"]
    
    for char in dangerous_chars:
        command = command.replace(char, '')
    
    return command.strip()

def validate_url(url: str) -> bool:
    """
    Basic URL validation
    """
    return url.startswith(('http://', 'https://'))

def get_system_info() -> Dict[str, Any]:
    """
    Get basic system information
    """
    import platform
    
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version()
    }

def create_directory_if_not_exists(path: str):
    """
    Create directory if it doesn't exist
    """
    os.makedirs(path, exist_ok=True)

def safe_file_operation(operation_func, *args, **kwargs):
    """
    Wrapper for safe file operations
    """
    try:
        return operation_func(*args, **kwargs)
    except Exception as e:
        logging.error(f"File operation failed: {e}")
        return None
