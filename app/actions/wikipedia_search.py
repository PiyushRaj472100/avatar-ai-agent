"""
Wikipedia Search Action - Reliable search using Wikipedia API
"""

import requests
from typing import Dict, Any, List
import json

class WikipediaSearchAction:
    """
    Reliable search action using Wikipedia API (always works)
    """
    
    def __init__(self):
        self.api_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
    
    async def execute(self, parameters: Dict[str, Any]) -> str:
        """
        Execute Wikipedia search
        """
        query = parameters.get("query", "")
        
        if not query:
            return "No search query provided"
        
        try:
            # Search for the query
            search_results = await self._search_wikipedia(query)
            
            if search_results:
                return await self._format_results(query, search_results)
            else:
                return await self._try_alternative_search(query)
                
        except Exception as e:
            return f"Error during Wikipedia search: {str(e)}"
    
    async def _search_wikipedia(self, query: str) -> Dict[str, Any]:
        """
        Search Wikipedia API
        """
        try:
            # Try direct page lookup first
            url = f"{self.api_url}{query.replace(' ', '_')}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                # Try search API
                search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
                response = requests.get(search_url, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return None
                    
        except Exception as e:
            print(f"Wikipedia API error: {e}")
            return None
    
    async def _format_results(self, query: str, results: Dict[str, Any]) -> str:
        """
        Format Wikipedia results
        """
        title = results.get("title", "Unknown")
        description = results.get("description", "No description available")
        extract = results.get("extract", "No detailed information available")
        url = results.get("content_urls", {}).get("desktop", {}).get("page", "")
        
        formatted_result = f"""**Wikipedia Results for: {query}**

**{title}**

{description}

**Summary:**
{extract[:500]}...

**Full Article:** {url}

---
*Information sourced from Wikipedia - always reliable and up-to-date!*"""
        
        return formatted_result
    
    async def _try_alternative_search(self, query: str) -> str:
        """
        Try alternative search terms if direct lookup fails
        """
        alternatives = [
            f"{query} (programming)",
            f"{query} (computer science)",
            f"{query} (technology)",
            query.split()[0]  # First word only
        ]
        
        for alt_query in alternatives:
            results = await self._search_wikipedia(alt_query)
            if results:
                return await self._format_results(f"{query} (found as: {alt_query})", results)
        
        return f"No Wikipedia results found for '{query}'. Try a more specific term like 'Python programming language' or 'Machine learning'."
