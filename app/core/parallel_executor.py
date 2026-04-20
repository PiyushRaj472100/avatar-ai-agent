"""
Parallel Executor - Non-blocking parallel execution for fast AI responses
"""

import threading
import time
import requests
from typing import Dict, Any, Optional
from app.brain.llm import LLMInterface

class ParallelExecutor:
    """
    Executes AI and search in parallel for instant responses
    """
    
    def __init__(self):
        self.llm = LLMInterface()
    
    def fast_search(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Fast search with 2-second timeout
        """
        try:
            response = requests.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": 1},
                timeout=2  # 🔥 KEY: 2-second timeout
            )
            if response.status_code == 200:
                return {"data": response.json(), "source": "search_api"}
        except:
            pass
        return None
    
    def fast_ai_response(self, query: str) -> str:
        """
        Instant Gemini response
        """
        try:
            return self.llm.generate_response(query)
        except:
            return "Processing your request..."
    
    def get_parallel_response(self, query: str, query_type: str) -> str:
        """
        Execute both AI and search in parallel, merge if needed
        """
        result = {"ai_answer": "", "search_data": None}
        
        def fetch_search():
            """Background search thread"""
            if query_type == "dynamic":
                result = self.fast_search(query)
                if result:
                    result["search_data"] = result
        
        # Start search in background immediately
        search_thread = threading.Thread(target=fetch_search)
        search_thread.start()
        
        # Get instant AI response (no blocking)
        result["ai_answer"] = self.fast_ai_response(query)
        
        # Wait max 2 seconds for search data
        search_thread.join(timeout=2)
        
        # Merge results if search data is available
        if result["search_data"]:
            return self._merge_results(result["ai_answer"], result["search_data"], query)
        
        # Return AI answer if no search data
        return result["ai_answer"]
    
    def _merge_results(self, ai_answer: str, search_data: Dict[str, Any], query: str) -> str:
        """
        Intelligence layer to merge AI knowledge with real search data
        """
        merge_prompt = f"""
        You are Avatar AI Agent. Enhance this answer using real search data:
        
        Original AI Answer:
        {ai_answer}
        
        Real Search Data:
        {search_data.get('data', {})}
        
        User Query: {query}
        
        Please provide:
        1. Enhanced answer using real data
        2. Working links from search results
        3. Current/relevant information
        """
        
        try:
            return self.llm.generate_response(merge_prompt)
        except:
            return ai_answer  # Fallback to original answer
