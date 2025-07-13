"""
Exa MCP Tool Wrapper

Thin wrapper for Exa search MCP server calls.
"""

import os
import requests
from crewai.tools import tool
from typing import Dict, Any, List

BASE_URL = os.getenv("EXA_MCP_URL", "http://localhost:8001")

@tool("exa.search")
def exa_search(query: str, location: str = "", date: str = "") -> List[Dict[str, Any]]:
    """Search for local experiences using Exa semantic search."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "search",
                "args": {
                    "query": query,
                    "location": location,
                    "date": date
                }
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        # Fallback data for testing
        return [
            {
                "name": "Adventure Photography Workshop",
                "location": "Golden Gate Park",
                "address": "Golden Gate Park, San Francisco, CA",
                "date": date or "2024-01-15",
                "time": "2:00 PM - 5:00 PM",
                "price": "$75",
                "description": "Learn adventure photography techniques in iconic locations",
                "relevance_score": 0.95,
                "categories": ["photography", "outdoor", "workshop"],
                "contact": "info@adventurephoto.com",
                "booking_url": "https://example.com/book",
                "error": str(e),
                "fallback": True
            },
            {
                "name": "Urban Exploration Tour",
                "location": "Mission District",
                "address": "Mission District, San Francisco, CA",
                "date": date or "2024-01-15",
                "time": "10:00 AM - 1:00 PM",
                "price": "$45",
                "description": "Guided tour of hidden gems and local culture",
                "relevance_score": 0.88,
                "categories": ["culture", "walking", "guided"],
                "contact": "tours@urbanexplorer.com",
                "booking_url": "https://example.com/book",
                "error": str(e),
                "fallback": True
            }
        ]

@tool("exa.find_events")
def exa_find_events(topics: List[str], location: str, date: str) -> List[Dict[str, Any]]:
    """Find local events matching specific topics."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "find_events",
                "args": {
                    "topics": topics,
                    "location": location,
                    "date": date
                }
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json().get("events", [])
    except Exception as e:
        # Use search fallback
        return exa_search(f"{' '.join(topics)}", location, date)