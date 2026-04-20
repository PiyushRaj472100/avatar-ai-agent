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
        You are Avatar AI Agent's decision-making brain. Analyze the user's command and decide which action to take.
        
        Available actions:
        - open_apps: Open applications (parameters: app_name, optional: url)
        - search_web: Search the web (parameters: query)
        - system_control: Control system functions (parameters: command)
        
        Respond with a JSON object containing:
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
        Simple fallback action mapping when LLM fails
        """
        command_lower = command.lower()
        
        if "open" in command_lower and ("chrome" in command_lower or "browser" in command_lower):
            return {"action": "open_apps", "parameters": {"app_name": "chrome"}}
        elif "search" in command_lower or "google" in command_lower:
            return {"action": "search_web", "parameters": {"query": command}}
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
