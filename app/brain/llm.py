"""
LLM Interface - Handles interaction with language models
"""

from app.core.config import settings
import google.generativeai as genai
import json
from typing import Dict, Any

class LLMInterface:
    """
    Interface for interacting with Large Language Models
    """
    
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.model_name)
        self.max_tokens = settings.max_tokens
        self.temperature = settings.temperature
    
    async def decide_action(self, command: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use LLM to decide which action to take based on the command and context
        """
        system_prompt = """
        You are Avatar AI Agent's decision-making brain. Think intelligently about user intent.
        
        CRITICAL RULES:
        1. For "find", "research", "compare", "best", "top" queries - USE search_summary
        2. search_summary returns analyzed data WITHOUT opening browser
        3. search_web opens browser - ONLY use when user explicitly asks to open/browse
        4. Think about what the user REALLY wants - information or action?
        
        Available actions:
        - search_summary: Intelligent search with analysis (parameters: query, engine, max_results)
        - wikipedia_search: Reliable Wikipedia search (parameters: query)
        - news_search: Real-time news search (parameters: query)
        - search_web: Open browser with search (parameters: query, engine)
        - open_apps: Open applications/websites (parameters: app_name, url)
        - system_control: Control system functions (parameters: command)
        
        Examples:
        "Find best Python course" -> search_summary
        "Compare laptops" -> search_summary
        "Open chrome" -> open_apps
        "Browse python tutorials" -> search_web
        
        Respond with JSON:
        {
            "action": "action_name",
            "parameters": {"key": "value"},
            "reasoning": "why this action was chosen"
        }
        """
        
        try:
            full_prompt = f"{system_prompt}\n\nCommand: {command}\nContext: {json.dumps(context, indent=2)}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
            )
            
            result = response.text.strip()
            
            # Parse JSON response
            return json.loads(result)
            
        except Exception as e:
            # Fallback to simple action mapping
            return self._fallback_action_mapping(command)
    
    def _fallback_action_mapping(self, command: str) -> Dict[str, Any]:
        """
        Intelligent fallback action mapping when LLM fails
        """
        command_lower = command.lower()
        
        # Handle "interested" requests with normal browser search
        if any(phrase in command_lower for phrase in ["interested", "tell me more", "more info", "search for", "learn more"]):
            return {"action": "search_web", "parameters": {"query": command}}
        # Handle open commands with link provision
        elif "open" in command_lower:
            clean_name = command_lower.replace("open", "").strip()
            return {"action": "open_apps", "parameters": {"app_name": clean_name}}
        elif any(word in command_lower for word in ["find", "research", "compare", "best", "top"]):
            return {"action": "search_summary", "parameters": {"query": command, "max_results": 5}}
        elif any(word in command_lower for word in ["what is", "define", "explain", "tell me about"]):
            return {"action": "search_summary", "parameters": {"query": command, "max_results": 5}}
        elif "browse" in command_lower or "search and browse" in command_lower:
            return {"action": "search_web", "parameters": {"query": command}}
        elif "wikipedia" in command_lower or "wiki" in command_lower:
            clean_query = command.replace("wikipedia", "").replace("wiki", "").replace("search", "").strip()
            return {"action": "wikipedia_search", "parameters": {"query": clean_query}}
        elif "news" in command_lower or "latest" in command_lower or "current" in command_lower:
            return {"action": "news_search", "parameters": {"query": command}}
        elif "search" in command_lower:
            return {"action": "search_summary", "parameters": {"query": command, "max_results": 3}}
        else:
            return {"action": "system_control", "parameters": {"command": command}}
    
    async def generate_response(self, prompt: str) -> str:
        """
        Generate a natural language response using the LLM
        """
        try:
            full_prompt = f"You are a helpful AI assistant.\n\nUser: {prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
