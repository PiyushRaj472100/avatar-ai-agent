"""
API routes for Avatar AI Agent
"""

from fastapi import APIRouter, HTTPException
from app.schemas.command_schema import CommandRequest, CommandResponse, AgentModeRequest
from app.agents.commander import CommanderAgent

router = APIRouter()
commander = CommanderAgent()

@router.post("/command", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    Execute a simple command through the AI agent
    """
    try:
        # Auto-detect if agent mode should be used
        use_agent_mode = await commander.should_use_agent_mode(request.command)
        
        response = await commander.process_command(request.command, use_agent_mode)
        
        return CommandResponse(
            success=True,
            response=response,
            message="Command executed successfully",
            action_taken="agent_mode" if use_agent_mode else "simple_command",
            debug_info=f"Command: {request.command}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Command execution failed: {str(e)}"
        )

@router.post("/agent", response_model=CommandResponse)
async def execute_agent_task(request: CommandRequest):
    """
    Execute a complex task using Agent Mode (multi-step planning and execution)
    """
    try:
        response = await commander.process_command(request.command, use_agent_mode=True)
        
        return CommandResponse(
            success=True,
            response=response,
            message="Agent task completed",
            action_taken="agent_mode"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent task execution failed: {str(e)}"
        )

@router.post("/simple", response_model=CommandResponse)
async def execute_simple_command(request: CommandRequest):
    """
    Execute a simple command without Agent Mode (forces simple execution)
    """
    try:
        response = await commander.process_command(request.command, use_agent_mode=False)
        
        return CommandResponse(
            success=True,
            response=response,
            message="Simple command executed",
            action_taken="simple_command"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Simple command execution failed: {str(e)}"
        )

@router.post("/confirm", response_model=CommandResponse)
async def handle_confirmation(request: CommandRequest):
    """
    Handle user confirmation for opening links
    """
    try:
        command = request.command.lower()
        
        if "yes" in command or "ok" in command or "sure" in command:
            # User confirmed - execute the pending action
            pending = commander.confirmation.get_pending_action("default")
            if pending:
                # Execute the pending action
                from app.actions.open_apps import OpenAppsAction
                open_apps = OpenAppsAction()
                result = await open_apps.execute({"app_name": pending["action"]})
                return CommandResponse(
                    success=True,
                    response=f"Opened {pending['action']} as requested",
                    message="Confirmation accepted - link opened",
                    action_taken="confirmed_open"
                )
            else:
                return CommandResponse(
                    success=False,
                    response="No pending action to confirm",
                    message="No pending action to confirm"
                )
        elif "no" in command or "cancel" in command or "stop" in command:
            # User cancelled - cancel the pending action
            pending = commander.confirmation.get_pending_action("default")
            if pending:
                commander.confirmation.cancel_action("default")
                return CommandResponse(
                    success=True,
                    response=f"Cancelled opening {pending['action']}",
                    message="Action cancelled as requested",
                    action_taken="cancelled_open"
                )
            else:
                return CommandResponse(
                    success=False,
                    response="Please respond with 'yes', 'ok', 'no', or 'cancel'",
                    message="Please confirm if you want to open the link"
                )
        else:
            return CommandResponse(
                success=True,
                response="Please respond with 'yes', 'ok', 'no', or 'cancel'",
                message="Please confirm if you want to open the link"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Confirmation handling failed: {str(e)}"
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
