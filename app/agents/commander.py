"""
Commander Agent - Brain decision layer for Avatar AI Agent
"""

from app.brain.llm import LLMInterface
from app.actions.open_apps import OpenAppsAction
from app.actions.search_web import SearchWebAction
from app.actions.search_summary import SearchSummaryAction
from app.actions.system_control import SystemControlAction
from app.memory.memory_manager import MemoryManager
from app.core.query_classifier import classify_query
from app.core.parallel_executor import ParallelExecutor
from typing import Dict, Any
from app.agents.agent_mode import AgentMode
from app.actions.confirmation_handler import ConfirmationHandler
import json

class CommanderAgent:
    """
    Main agent that processes commands and decides which actions to execute
    Supports both simple commands and complex agent mode tasks
    """
    
    def __init__(self):
        self.llm = LLMInterface()
        self.memory = MemoryManager()
        self.confirmation = ConfirmationHandler()
        self.parallel_executor = ParallelExecutor()
        
        # Initialize available actions
        self.actions = {
            "open_apps": OpenAppsAction(),
            "search_web": SearchWebAction(),
            "search_summary": SearchSummaryAction(),
            "system_control": SystemControlAction()
        }
        
        # Agent mode
        self.agent_mode = AgentMode(self.actions)
    
    async def process_command(self, command: str, use_agent_mode: bool = False) -> str:
        """
        Process a user command and execute the appropriate action
        
        Args:
            command: The user's command
            use_agent_mode: Whether to use agent mode for complex tasks
        """
        try:
            if use_agent_mode:
                # Use Agent Mode for complex multi-step tasks
                result = await self.agent_mode.execute_task(command)
                return json.dumps(result, indent=2)
            else:
                # Simple command processing (original behavior)
                return await self._process_simple_command(command)
                
        except Exception as e:
            return f"Error processing command: {str(e)}"
    
    async def _process_simple_command(self, command: str) -> str:
        """
        Process a simple command using new non-blocking architecture
        """
        try:
            # Get context from memory
            context = self.memory.get_context()
            
            # Direct routing for app and interest commands (instant)
            command_lower = command.lower()
            if "open" in command_lower:
                clean_name = command_lower.replace("open", "").strip()
                action = self.actions["open_apps"]
                return await action.execute({"app_name": clean_name})
            elif any(phrase in command_lower for phrase in ["interested", "tell me more", "more info"]):
                action = self.actions["search_web"]
                return await action.execute({"query": command})
            
            # Classify query type for intelligent handling
            query_type = classify_query(command)
            
            if query_type == "dynamic":
                # Use parallel execution for dynamic queries (best, compare, latest)
                print(f"Dynamic query detected: {command} - using parallel execution")
                return self.parallel_executor.get_parallel_response(command, query_type)
            else:
                # Use fast AI response for static queries (what is, explain, define)
                print(f"Static query detected: {command} - using AI knowledge")
                return await self.llm.generate_response(command)
                
        except Exception as e:
            return f"Error processing command: {str(e)}"
    
    async def should_use_agent_mode(self, command: str) -> bool:
        """
        Decide if a command requires agent mode based on complexity
        """
        system_prompt = """
        You are Avatar AI Agent deciding whether to use Agent Mode.
        
        Agent Mode is for complex, multi-step tasks like:
        - "Find and open the best Python course"
        - "Research and compare 3 laptops"
        - "Plan a weekend trip to Paris"
        - "Find a recipe and open shopping list"
        
        Simple commands use normal mode:
        - "open chrome"
        - "search for python"
        - "shutdown computer"
        
        Command: {command}
        
        Return JSON: {{"use_agent_mode": true/false, "reasoning": "why"}}
        """.format(command=command)
        
        try:
            response = self.llm.model.generate_content(system_prompt)
            decision = json.loads(response.text.strip())
            return decision.get("use_agent_mode", False)
        except:
            # Fallback: use simple heuristics
            return len(command.split()) > 8 or "and" in command.lower() or "then" in command.lower()
