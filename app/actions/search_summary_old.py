"""
Search Summary Action - Search API + Gemini intelligent analysis
"""

from app.brain.llm import LLMInterface
import requests
from typing import Dict, Any, List
import json

class SearchSummaryAction:
    """
    Smart search action that analyzes and summarizes results without opening browser
    """
    
    def __init__(self):
        self.llm = LLMInterface()
        # Search API configuration (using DuckDuckGo for now - free and reliable)
        self.search_api_url = "https://api.duckduckgo.com/"
        self.backup_search = "https://duckduckgo.com/html/?q="
    
    async def execute(self, parameters: Dict[str, Any]) -> str:
        """
        Execute intelligent search with analysis and summarization
        """
        query = parameters.get("query", "")
        engine = parameters.get("engine", "google").lower()
        max_results = parameters.get("max_results", 5)
        
        if not query:
            return "No search query provided"
        
        try:
            # Step 1: Get search results from Search API
            search_results = await self._get_search_api_results(query, max_results)
            
            if not search_results:
                # Use Gemini knowledge for general knowledge queries
                return await self._gemini_knowledge_fallback(query)
            
            # Step 2: Analyze and compare using Gemini with real data
            analysis = await self._analyze_with_real_data(query, search_results)
            
            return analysis
            
        except Exception as e:
            return f"Error during intelligent search: {str(e)}"
    
    async def _gemini_knowledge_fallback(self, query: str) -> str:
        """
        When web scraping fails, use Gemini's knowledge to provide helpful information
        """
        system_prompt = f"""
        You are Avatar AI Agent providing expert knowledge when web search is unavailable.
        
        User Query: {query}
        
        Since web search is not available, provide your knowledge-based recommendations.
        
        For course/learning queries, include:
        1. Top well-known platforms (Coursera, edX, Udemy, etc.)
        2. Specific highly-rated courses
        3. Key features and pricing information
        4. Skill level and prerequisites
        5. Why you recommend each option
        
        For other queries, provide:
        1. Best known solutions/tools
        2. Key features and comparisons
        3. Pricing and availability
        4. Pros and cons
        5. Recommendations based on common use cases
        
        Be specific, practical, and helpful. Acknowledge that this is based on your training knowledge.
        """
        
        try:
            response = self.llm.model.generate_content(system_prompt)
            return response.text.strip()
        except Exception as e:
            # Dynamic fallback based on query
            if "python course" in query.lower():
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

4. **Google's Python Class** (Free)
   - Technical focus
   - Good for developers
   - Includes exercises
   - **Link**: https://developers.google.com/edu/python

5. **MIT Introduction to Python** (edX)
   - Academic approach
   - Rigorous curriculum
   - Free access
   - **Link**: https://www.edx.org/course/introduction-computer-science-and-programming

**Additional Resources:**
- **Python Documentation**: https://docs.python.org/3/
- **Real Python**: https://realpython.com/
- **Python.org Tutorial**: https://docs.python.org/3/tutorial/

I recommend starting with 'Python for Everybody' if you're new to programming, or 'Complete Python Bootcamp' if you want comprehensive hands-on learning.

*Say "open [course name]" and I'll open the link for you!*"""
            elif "laptop" in query.lower():
                return """Here are some excellent laptop recommendations for students:

**Best Student Laptops:**

1. **MacBook Air M2** (Premium Choice)
   - Excellent battery life (15+ hours)
   - Lightweight and portable
   - Great performance for coding and studies
   - Price: $999-$1299
   - **Link**: https://www.apple.com/macbook-air-m2

2. **Dell XPS 13** (Windows Alternative)
   - Powerful performance in compact size
   - Excellent display and build quality
   - Great for engineering students
   - Price: $800-$1200
   - **Link**: https://www.dell.com/en-us/shop/dell-laptops/xps-13-laptop

3. **Lenovo ThinkPad X1 Carbon** (Business/CS Students)
   - Legendary keyboard comfort
   - Durable and reliable
   - Great for programming
   - Price: $1000-$1400
   - **Link**: https://www.lenovo.com/us/en/p/thinkpad/x1-carbon-gen-11

4. **HP Pavilion Aero 13** (Budget-Friendly)
   - Great value for money
   - Lightweight (under 3 lbs)
   - Good performance for everyday tasks
   - Price: $600-$800
   - **Link**: https://www.hp.com/us-en/p/pavilion-laptops

5. **ASUS ZenBook 14** (Best Value)
   - Excellent performance for price
   - OLED display option available
   - Great for multimedia and coding
   - Price: $700-$900
   - **Link**: https://www.asus.com/us/zenbook/

**Where to Buy:**
- **Amazon**: https://www.amazon.com/best-sellers-computers-laptops
- **Best Buy**: https://www.bestbuy.com/site/computers-pcs
- **Newegg**: https://www.newegg.com/Laptops/Category/ID-226

**My Recommendation:** 
- For CS/Engineering: Dell XPS 13 or MacBook Air M2
- For Budget: HP Pavilion Aero 13
- For General Studies: ASUS ZenBook 14

**Important Specs:**
- RAM: 8GB minimum, 16GB recommended
- Storage: SSD (256GB minimum)
- Battery: 8+ hours preferred
- Weight: Under 4 lbs for portability

*Say "open [laptop name]" and I'll open the product page for you!*"""
            elif "vacation" in query.lower() and "india" in query.lower():
                return """Here are some excellent monsoon vacation destinations in India:

**Top Monsoon Vacation Spots in India:**

1. **Munnar, Kerala** - Tea Gardens & Waterfalls
   - Lush green tea plantations
   - Beautiful waterfalls (Attukal, Lakkam)
   - Cool, pleasant weather
   - **Link**: https://www.keralatourism.org/destination/munnar/

2. **Lonavala, Maharashtra** - Hill Station Near Mumbai
   - Scenic valleys and waterfalls
   - Perfect weekend getaway
   - Misty mountains and lakes
   - **Link**: https://www.maharashtratourism.gov.in/destination/lonavala

3. **Coorg, Karnataka** - Coffee Plantations
   - Misty hills and coffee estates
   - Abbey Falls and Iruppu Falls
   - Pleasant climate
   - **Link**: https://www.karnatakatourism.org/tourist-places/coorg/

4. **Mahabaleshwar, Maharashtra** - Strawberry Paradise
   - Strawberry farms
   - Venna Lake and viewpoints
   - Cool climate
   - **Link**: https://www.maharashtratourism.gov.in/destination/mahabaleshwar

5. **Shillong, Meghalaya** - Scotland of the East
   - Living root bridges
   - Waterfalls and lakes
   - Pleasant monsoon weather
   - **Link**: https://www.meghalayatourism.in/

**Travel Resources:**
- **MakeMyTrip**: https://www.makemytrip.com/
- **IRCTC Tourism**: https://www.irctctourism.com/
- **Yatra**: https://www.yatra.com/

*If you're interested in any of these destinations, I can do a normal browser search for more detailed information!*"""
        else:
            return f"I'm unable to search the web right now, but based on my knowledge, I can help with '{query}'. Please try again later for real-time search results, or ask me a more specific question about this topic."""

async def _get_search_api_results(self, query: str, max_results: int) -> List[Dict[str, Any]]:
    """
    Get search results from Search API (DuckDuckGo API - free and reliable)
    """
    try:
        # Use DuckDuckGo Instant Answer API
        params = {
            'q': query,
            'format': 'json',
            'no_html': 1,
            'skip_disambig': 1
        }
        
        response = requests.get(self.search_api_url, params=params, timeout=10)
        
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
        
        # Find search result divs
        search_divs = soup.find_all('div', class_='result')
        
        for i, div in enumerate(search_divs[:max_results]):
            try:
                # Extract title and link
                title_elem = div.find('a', class_='result__a')
                if title_elem:
                    title = title_elem.get_text().strip()
                    link = title_elem.get('href', '')
                    
                    # Extract description
                    desc_elem = div.find('a', class_='result__snippet')
                    description = desc_elem.get_text().strip() if desc_elem else "No description"
                    
                    if title and link:
                        results.append({
                            "title": title,
                            "link": link,
                            "description": description
                        })
                        
            except Exception as e:
                continue
        
        return results
    
    def _parse_google_results(self, soup: BeautifulSoup, max_results: int) -> List[Dict[str, Any]]:
        """
        Parse Google search results
        """
        results = []
        
        # Find search result divs
        search_divs = soup.find_all('div', class_=re.compile(r'g|tF2Cxc'))
        
        for i, div in enumerate(search_divs[:max_results]):
            try:
                # Extract title
                title_elem = div.find('h3')
                title = title_elem.get_text() if title_elem else "No title"
                
                # Extract link
                link_elem = div.find('a')
                link = link_elem.get('href', '') if link_elem else ''
                
                # Extract description
                desc_elem = div.find('span', class_=re.compile(r'aCOpRe|st'))
                description = desc_elem.get_text() if desc_elem else "No description"
                
                if title and link and title != "No title":
                    results.append({
                        "title": title.strip(),
                        "link": link,
                        "description": description.strip()
                    })
                    
            except Exception as e:
                continue
        
        return results
    
    def _parse_bing_results(self, soup: BeautifulSoup, max_results: int) -> List[Dict[str, Any]]:
        """
        Parse Bing search results
        """
        results = []
        
        # Find search result divs
        search_divs = soup.find_all('li', class_='b_algo')
        
        for i, div in enumerate(search_divs[:max_results]):
            try:
                # Extract title and link
                title_elem = div.find('h2')
                if title_elem:
                    link_elem = title_elem.find('a')
                    title = title_elem.get_text().strip()
                    link = link_elem.get('href', '') if link_elem else ''
                    
                    # Extract description
                    desc_elem = div.find('p')
                    description = desc_elem.get_text().strip() if desc_elem else "No description"
                    
                    if title and link:
                        results.append({
                            "title": title,
                            "link": link,
                            "description": description
                        })
                        
            except Exception as e:
                continue
        
        return results
    
    async def _analyze_results(self, query: str, results: List[Dict[str, Any]]) -> str:
        """
        Use LLM to analyze and summarize search results
        """
        # Format results for LLM
        results_text = "\n".join([
            f"{i+1}. {result['title']}\n   {result['description']}\n   Link: {result['link']}"
            for i, result in enumerate(results)
        ])
        
        system_prompt = f"""
        You are Avatar AI Agent's intelligent search analyst. Analyze these search results and provide a comprehensive summary.
        
        User Query: {query}
        
        Search Results:
        {results_text}
        
        Provide:
        1. A clear summary of the top results
        2. Comparison if relevant (for "best", "compare", "vs" queries)
        3. Key insights and recommendations
        4. Specific details from the most relevant results
        
        Be helpful, specific, and analytical. Don't just list results - provide actual intelligence.
        """
        
        try:
            response = self.llm.model.generate_content(system_prompt)
            return response.text.strip()
        except Exception as e:
            # Fallback: simple formatting
            return f"Found {len(results)} results for '{query}'. Top results:\n{results_text}"
