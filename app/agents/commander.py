"""
Commander Agent - Brain decision layer for Avatar AI Agent
"""

from app.brain.llm import LLMInterface
from app.actions.open_apps import OpenAppsAction
from app.actions.search_web import SearchWebAction
from app.actions.search_summary import SearchSummaryAction
from app.actions.wikipedia_search import WikipediaSearchAction
from app.actions.news_search import NewsSearchAction
from app.actions.system_control import SystemControlAction
from app.memory.memory_manager import MemoryManager
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
        self.agent_mode = AgentMode()
        self.confirmation = ConfirmationHandler()
        
        # Initialize available actions
        self.actions = {
            "open_apps": OpenAppsAction(),
            "search_web": SearchWebAction(),
            "search_summary": SearchSummaryAction(),
            "wikipedia_search": WikipediaSearchAction(),
            "news_search": NewsSearchAction(),
            "system_control": SystemControlAction()
        }
    
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
        Process a simple command (original functionality)
        """
        try:
            # Get context from memory
            context = self.memory.get_context()
            
            # Direct routing for speed - skip LLM for common patterns
            command_lower = command.lower()
            if any(word in command_lower for word in ["best", "compare", "top", "find", "research"]):
                action_decision = {"action": "search_summary", "parameters": {"query": command, "max_results": 5}}
            elif any(word in command_lower for word in ["vacation", "travel", "tourism", "india", "monsoon"]):
                action_decision = {"action": "search_summary", "parameters": {"query": command, "max_results": 5}}
            elif any(word in command_lower for word in ["what is", "define", "explain", "tell me about"]):
                action_decision = {"action": "search_summary", "parameters": {"query": command, "max_results": 5}}
            elif "open" in command_lower:
                clean_name = command_lower.replace("open", "").strip()
                action_decision = {"action": "open_apps", "parameters": {"app_name": clean_name}}
            elif any(phrase in command_lower for phrase in ["interested", "tell me more", "more info"]):
                action_decision = {"action": "search_web", "parameters": {"query": command}}
            else:
                # Use LLM only for complex/unclear commands
                action_decision = await self.llm.decide_action(command, context)
            
            # Parse the action decision
            action_name = action_decision.get("action")
            action_params = action_decision.get("parameters", {})
            
            # Debug logging
            print(f"LLM Decision: {action_name} for command: {command}")
            
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
