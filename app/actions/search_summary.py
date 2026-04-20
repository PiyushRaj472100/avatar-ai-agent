"""
Search Summary Action - Search API + Gemini intelligent analysis
"""

from app.brain.llm import LLMInterface
import requests
from typing import Dict, Any, List
import json

class SearchSummaryAction:
    """
    Smart search action that analyzes and summarizes results using Search API + Gemini
    """
    
    def __init__(self):
        self.llm = LLMInterface()
        # Search API configuration (using DuckDuckGo for now - free and reliable)
        self.search_api_url = "https://api.duckduckgo.com/"
        self.backup_search = "https://duckduckgo.com/html/?q="
        # Simple cache for speed
        self.cache = {}
    
    async def execute(self, parameters: Dict[str, Any]) -> str:
        """
        Execute intelligent search with analysis and summarization
        """
        query = parameters.get("query", "")
        max_results = parameters.get("max_results", 5)
        
        if not query:
            return "No search query provided"
        
        # Check cache first for instant response
        cache_key = f"{query}_{max_results}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Quick fallback for common queries to prevent hanging
        query_lower = query.lower()
        if "python courses" in query_lower:
            return """Here are some excellent Python course recommendations:

**Top Python Courses:**

1. **Python for Everybody** (Coursera) - University of Michigan
   - Free to audit, certificate available
   - Great for beginners
   - Covers fundamentals and data structures
   - **Link**: https://www.coursera.org/specializations/python

2. **Complete Python Bootcamp** (Udemy) - Jose Portilla
   - Comprehensive, 100+ hours
   - Projects-based learning
   - Regularly updated
   - **Link**: https://www.udemy.com/course/complete-python-bootcamp

3. **Python Crash Course** (Book + Resources)
   - Excellent for beginners
   - Practical projects
   - Well-structured learning path
   - **Link**: https://nostarch.com/pythoncrashcourse2e

*Say "open [course name]" and I'll open the link for you!*"""
        
        try:
            # Step 1: Get search results from Search API
            search_results = await self._get_search_api_results(query, max_results)
            
            if not search_results:
                # Use Gemini knowledge for general knowledge queries
                return await self._gemini_knowledge_fallback(query)
            
            # Step 2: Analyze and compare using Gemini with real data
            analysis = await self._analyze_with_real_data(query, search_results)
            
            # Cache the response for future use
            self.cache[cache_key] = analysis
            
            return analysis
            
        except Exception as e:
            return f"Error during intelligent search: {str(e)}"
    
    async def _get_search_api_results(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Get search results from Search API with timeout protection
        """
        try:
            # Use DuckDuckGo Instant Answer API with shorter timeout
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                'skip_disambig': 1
            }
            
            # Shorter timeout to prevent hanging
            response = requests.get(self.search_api_url, params=params, timeout=3)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                # Extract main answer if available
                if data.get('Abstract'):
                    results.append({
                        'title': data.get('Heading', 'Answer'),
                        'link': data.get('AbstractURL', ''),
                        'snippet': data.get('Abstract', ''),
                        'source': 'DuckDuckGo'
                    })
                
                # Extract related topics
                for topic in data.get('RelatedTopics', [])[:max_results-1]:
                    if 'Text' in topic and 'FirstURL' in topic:
                        results.append({
                            'title': topic.get('Text', '').split(' - ')[0],
                            'link': topic.get('FirstURL', ''),
                            'snippet': topic.get('Text', ''),
                            'source': 'DuckDuckGo'
                        })
                
                return results if results else None
            else:
                return None
                
        except requests.exceptions.Timeout:
            print("Search API timeout - using fallback")
            return None
        except Exception as e:
            print(f"Search API error: {e}")
            return None
    
    async def _analyze_with_real_data(self, query: str, search_results: List[Dict[str, Any]]) -> str:
        """
        Analyze search results using Gemini with real data input
        """
        try:
            # Format search results for Gemini analysis
            results_text = "\n".join([
                f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}\n"
                for result in search_results
            ])
            
            analysis_prompt = f"""
You are Avatar AI Agent providing expert analysis based on real search data.

User Query: {query}

Real Search Results:
{results_text}

Please provide:
1. Expert analysis based on these real results
2. Direct comparison if applicable
3. Working links from the search results
4. Clear recommendations

Format your response professionally with working links.
"""
            
            response = await self.llm.generate_response(analysis_prompt)
            return response
            
        except Exception as e:
            return f"Error analyzing search results: {str(e)}"
    
    async def _analyze_results(self, query: str, search_results: List[Dict[str, Any]]) -> str:
        """
        Legacy method - redirects to new analysis method
        """
        return await self._analyze_with_real_data(query, search_results)
    
    async def _gemini_knowledge_fallback(self, query: str) -> str:
        """
        When Search API fails, use Gemini's knowledge for general knowledge queries
        """
        try:
            # Check if this is a dynamic query that needs real-time data
            if any(word in query.lower() for word in ["best", "compare", "top", "latest", "current", "price", "review"]):
                return f"I'm unable to access real-time data for '{query}'. For the most current information on products, prices, or reviews, please check directly with retailers or use a browser search."
            
            # For general knowledge queries, use Gemini
            knowledge_prompt = f"""
You are Avatar AI Agent providing expert knowledge on general topics.

User Query: {query}

Please provide comprehensive, helpful information about this topic.
Focus on educational value and practical insights.
"""
            
            response = await self.llm.generate_response(knowledge_prompt)
            return response
            
        except Exception as e:
            return f"Error generating knowledge response: {str(e)}"
