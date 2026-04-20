"""
Query Classifier - Fast query type detection for non-blocking AI responses
"""

from typing import Literal

def classify_query(query: str) -> Literal["dynamic", "static"]:
    """
    Classify query type to determine if real data is needed
    
    Dynamic queries need real-time data (prices, latest, best, compare)
    Static queries can use Gemini knowledge (what is, explain, define)
    """
    query_lower = query.lower()
    
    # Keywords that indicate need for real-time data
    dynamic_keywords = [
        "best", "top", "compare", "latest", "news", "price", 
        "current", "recent", "new", "deals", "discount",
        "review", "rating", "available", "stock", "sale"
    ]
    
    # Check if any dynamic keyword is present
    for keyword in dynamic_keywords:
        if keyword in query_lower:
            return "dynamic"
    
    # Default to static for knowledge-based queries
    return "static"
