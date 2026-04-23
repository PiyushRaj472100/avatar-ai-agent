"""
LLM Interface - Handles interaction with language models (FIXED)
"""

from app.core.config import settings
import google.generativeai as genai
import json
from typing import Dict, Any
import asyncio

class LLMInterface:
    """
    Interface for interacting with Large Language Models
    """
    
    def __init__(self):
        try:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.model_name)
            self.max_tokens = settings.max_tokens
            self.temperature = settings.temperature
            self.available = True
        except Exception as e:
            print(f"Gemini initialization failed: {e}")
            self.available = False
    
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
    
    def generate_response_sync(self, prompt: str) -> str:
        """
        Generate a response using Gemini (synchronous)
        """
        if not self.available:
            return "AI service temporarily unavailable. Using fallback responses."
        
        try:
            full_prompt = f"You are Avatar AI Agent. Provide helpful, accurate responses.\n\nUser: {prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            print(f"Gemini error: {e}")
            return self._fallback_response(prompt)
    
    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response using Gemini (async wrapper)
        """
        try:
            # Run sync Gemini in thread pool to avoid blocking
            return await asyncio.to_thread(self.generate_response_sync, prompt)
        except Exception as e:
            print(f"Async Gemini error: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """
        Fallback response when Gemini fails
        """
        prompt_lower = prompt.lower()
        
        # Static knowledge fallbacks
        if "machine learning" in prompt_lower:
            return """Machine Learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make decisions with minimal human intervention.

Key concepts include:
- Supervised Learning (learning from labeled data)
- Unsupervised Learning (finding patterns in unlabeled data)
- Reinforcement Learning (learning through rewards/penalties)
- Neural Networks (brain-inspired computing)

Common applications: image recognition, natural language processing, recommendation systems, and predictive analytics."""
        
        elif "python" in prompt_lower and "course" in prompt_lower:
            return """Here are some excellent Python learning resources:

**Top Python Courses:**
1. **Python for Everybody** (Coursera) - University of Michigan
2. **Complete Python Bootcamp** (Udemy) - Jose Portilla  
3. **Python Crash Course** (Book) - Eric Matthes
4. **Google's Python Class** - Free online course
5. **Codecademy Python** - Interactive learning

**Key Topics to Learn:**
- Python basics and syntax
- Data structures (lists, dictionaries, sets)
- Functions and modules
- Object-oriented programming
- File handling and exceptions
- Popular libraries (NumPy, Pandas, Flask)"""
        
        elif "best laptop" in prompt_lower:
            return """For laptop recommendations, I'd suggest considering:

**Top Laptop Categories:**
- **Budget**: Acer Aspire, HP Pavilion ($400-700)
- **Mid-range**: Dell Inspiron, Lenovo IdeaPad ($700-1000)  
- **Premium**: Dell XPS, MacBook Air/Pro ($1000+)
- **Gaming**: ASUS ROG, MSI gaming laptops

**Key Factors:**
- CPU: Intel i5/i7 or AMD Ryzen 5/7
- RAM: 8GB minimum, 16GB recommended
- Storage: SSD for speed, 256GB minimum
- Battery: 8+ hours for portability
- Display: 1080p resolution minimum

For specific current models and prices, I'd recommend checking recent reviews as laptop models change frequently."""
        
        else:
            return f"I understand you're asking about: {prompt}\n\nI'm currently experiencing some technical difficulties with my AI service. For the most accurate and up-to-date information on this topic, I'd recommend:\n\n1. Searching online for recent information\n2. Checking official documentation\n3. Looking at educational resources specific to your topic\n\nI apologize for the inconvenience and appreciate your patience!"
