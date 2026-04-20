"""
Commander Agent - Brain decision layer for Avatar AI Agent
"""

from app.brain.llm import LLMInterface
from app.actions.open_apps import OpenAppsAction
from app.actions.search_web import SearchWebAction
from app.actions.system_control import SystemControlAction
from app.memory.memory_manager import MemoryManager
import json

class CommanderAgent:
    """
    Main agent that processes commands and decides which actions to execute
    """
    
    def __init__(self):
        self.llm = LLMInterface()
        self.memory = MemoryManager()
        
        # Initialize available actions
        self.actions = {
            "open_apps": OpenAppsAction(),
            "search_web": SearchWebAction(),
            "system_control": SystemControlAction()
        }
    
    async def process_command(self, command: str) -> str:
        """
        Process a user command and execute the appropriate action
        """
        try:
            # Get context from memory
            context = self.memory.get_context()
            
            # Use LLM to decide which action to take
            action_decision = await self.llm.decide_action(command, context)
            
            # Parse the action decision
            action_name = action_decision.get("action")
            action_params = action_decision.get("parameters", {})
            
            # Execute the action
            if action_name in self.actions:
                result = await self.actions[action_name].execute(action_params)
                
                # Store the interaction in memory
                self.memory.store_interaction(command, action_name, result)
                
                return result
            else:
                return f"Unknown action: {action_name}"
                
        except Exception as e:
            return f"Error processing command: {str(e)}"
