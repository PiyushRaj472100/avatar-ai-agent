"""
Async Executor - True non-blocking parallel execution
"""

import asyncio
import httpx
from app.brain.llm import LLMInterface

class AsyncExecutor:
    """
    True async execution - no blocking calls
    """
    
    def __init__(self):
        self.llm = LLMInterface()
    
    async def fast_ai_response(self, query: str) -> str:
        """
        Non-blocking Gemini call using asyncio.to_thread
        """
        try:
            # Wrap sync Gemini call in async thread
            return await asyncio.to_thread(self.llm.generate_response, query)
        except Exception as e:
            print(f"Gemini error: {e}")
            return "Processing your request..."
    
    async def search_web_async(self, query: str) -> dict:
        """
        Non-blocking search using httpx (async requests)
        """
        try:
            async with httpx.AsyncClient(timeout=2) as client:
                response = await client.get(
                    "https://api.duckduckgo.com/",
                    params={"q": query, "format": "json", "no_html": 1}
                )
                if response.status_code == 200:
                    return {"data": response.json(), "source": "search_api"}
        except Exception as e:
            print(f"Search error: {e}")
        return None
    
    async def get_parallel_response(self, query: str, query_type: str) -> str:
        """
        True parallel execution - NO BLOCKING
        """
        if query_type == "static":
            # Static queries: just AI (fast)
            print(f"Static query: {query} - AI only")
            return await self.fast_ai_response(query)
        
        # Dynamic queries: parallel AI + search
        print(f"Dynamic query: {query} - parallel execution")
        
        # Create tasks (this is NON-BLOCKING)
        ai_task = asyncio.create_task(self.fast_ai_response(query))
        search_task = asyncio.create_task(self.search_web_async(query))
        
        # Wait for completion with timeout (NON-BLOCKING)
        try:
            done, pending = await asyncio.wait(
                [ai_task, search_task],
                timeout=2.0,
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Get AI result (should be done first)
            ai_result = await ai_task
            
            # Check if search completed
            if search_task in done:
                search_result = search_task.result()
                if search_result:
                    return await self.merge_results(ai_result, search_result, query)
            
            # Return AI answer if search not ready
            return ai_result
            
        except asyncio.TimeoutError:
            print("Timeout - returning AI answer")
            # Return AI answer even if not ready
            ai_result = await ai_task
            return ai_result
    
    async def merge_results(self, ai_answer: str, search_data: dict, query: str) -> str:
        """
        Non-blocking result merging
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
            # Wrap merge in async thread (non-blocking)
            return await asyncio.to_thread(self.llm.generate_response, merge_prompt)
        except:
            return ai_answer  # Fallback to original
