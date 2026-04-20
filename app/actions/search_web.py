"""
Search Web Action - Performs web searches
"""

import webbrowser
from typing import Dict, Any

class SearchWebAction:
    """
    Action for performing web searches
    """
    
    def __init__(self):
        self.search_engines = {
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "duckduckgo": "https://duckduckgo.com/?q="
        }
    
    async def execute(self, parameters: Dict[str, Any]) -> str:
        """
        Execute the web search action
        """
        query = parameters.get("query", "")
        engine = parameters.get("engine", "google").lower()
        
        if not query:
            return "No search query provided"
        
        try:
            # Construct search URL
            if engine in self.search_engines:
                search_url = self.search_engines[engine] + query.replace(" ", "+")
            else:
                # Default to Google
                search_url = self.search_engines["google"] + query.replace(" ", "+")
            
            # Open in default browser
            webbrowser.open(search_url)
            
            return f"Searching for '{query}' using {engine}"
            
        except Exception as e:
            return f"Error performing search: {str(e)}"
