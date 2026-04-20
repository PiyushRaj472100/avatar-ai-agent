"""
API routes for Avatar AI Agent
"""

from fastapi import APIRouter, HTTPException
from app.schemas.command_schema import CommandRequest, CommandResponse
from app.agents.commander import CommanderAgent

router = APIRouter()
commander = CommanderAgent()

@router.post("/command", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    Execute a command through the AI agent
    """
    try:
        response = await commander.process_command(request.command)
        return CommandResponse(
            success=True,
            response=response,
            message="Command executed successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Command execution failed: {str(e)}"
        )

@router.get("/status")
async def get_status():
    """
    Get the current status of the AI agent
    """
    return {
        "status": "active",
        "agent": "Avatar AI Agent",
        "version": "1.0.0"
    }
