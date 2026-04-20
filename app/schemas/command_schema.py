"""
Command Schema - Data validation for API requests
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

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

class AgentModeRequest(BaseModel):
    """
    Schema for Agent Mode requests (complex multi-step tasks)
    """
    task: str = Field(..., description="The complex task to execute", min_length=1, max_length=1000)
    max_iterations: Optional[int] = Field(default=10, description="Maximum iterations for the agent loop")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context for the task")

class AgentStep(BaseModel):
    """
    Schema for individual agent steps
    """
    step_number: int = Field(..., description="Step number in the plan")
    description: str = Field(..., description="Description of what to do")
    tool: str = Field(..., description="Tool to use")
    parameters: Dict[str, Any] = Field(..., description="Parameters for the tool")
    expected_outcome: str = Field(..., description="Expected outcome of this step")

class AgentObservation(BaseModel):
    """
    Schema for agent observations (results of executed steps)
    """
    step_number: int = Field(..., description="Step number")
    description: str = Field(..., description="Step description")
    tool: str = Field(..., description="Tool that was used")
    parameters: Dict[str, Any] = Field(..., description="Parameters that were used")
    result: str = Field(..., description="Result of the execution")
    timestamp: str = Field(..., description="When this observation was made")
    error: Optional[bool] = Field(default=False, description="Whether this step had an error")

class AgentModeResponse(BaseModel):
    """
    Schema for Agent Mode responses
    """
    success: bool = Field(..., description="Whether the agent task was successful")
    task: str = Field(..., description="The original task")
    agent_mode: bool = Field(default=True, description="This was executed in agent mode")
    plan: List[AgentStep] = Field(..., description="The plan that was created")
    completed_steps: List[int] = Field(..., description="List of completed step numbers")
    observations: List[AgentObservation] = Field(..., description="Results from executed steps")
    final_result: str = Field(..., description="Final result and summary")
    is_complete: bool = Field(..., description="Whether the task was completed successfully")
    iterations_used: int = Field(..., description="Number of iterations used")
    summary: Dict[str, Any] = Field(..., description="Summary statistics")

class StatusResponse(BaseModel):
    """
    Schema for status responses
    """
    status: str = Field(..., description="Current status of the agent")
    agent: str = Field(..., description="Agent name")
    version: str = Field(..., description="Agent version")
    uptime: Optional[str] = Field(default=None, description="How long the agent has been running")
    memory_usage: Optional[Dict[str, Any]] = Field(default=None, description="Memory usage statistics")
