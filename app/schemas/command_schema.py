"""
Command Schema - Data validation for API requests
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class CommandRequest(BaseModel):
    """
    Schema for command requests
    """
    command: str = Field(..., description="The command to execute", min_length=1, max_length=1000)
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context for the command")

class CommandResponse(BaseModel):
    """
    Schema for command responses
    """
    success: bool = Field(..., description="Whether the command was successful")
    response: str = Field(..., description="The response from the command execution")
    message: Optional[str] = Field(default=None, description="Additional message about the execution")
    action_taken: Optional[str] = Field(default=None, description="The action that was taken")
    timestamp: Optional[str] = Field(default=None, description="Timestamp of the response")

class StatusResponse(BaseModel):
    """
    Schema for status responses
    """
    status: str = Field(..., description="Current status of the agent")
    agent: str = Field(..., description="Agent name")
    version: str = Field(..., description="Agent version")
    uptime: Optional[str] = Field(default=None, description="How long the agent has been running")
    memory_usage: Optional[Dict[str, Any]] = Field(default=None, description="Memory usage statistics")
