"""
MCP Tools Package

This module contains CrewAI tool wrappers for Model Context Protocol servers.
Each tool provides a standardized interface to external services.
"""

import os
import json
import requests
from typing import Dict, Any, List, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class YouTubeMCPTool(BaseTool):
    """
    Tool for interacting with YouTube content via MCP server.
    Provides video analysis, caption extraction, and metadata retrieval.
    """
    
    name: str = "youtube_mcp"
    description: str = """
    Analyze YouTube videos and extract insights.
    
    Capabilities:
    - Extract video captions/transcripts
    - Get video metadata (title, description, tags)
    - Analyze content themes and topics
    - Extract actionable insights for experience planning
    """
    
    def _run(self, video_url: str, analysis_type: str = "full") -> str:
        """
        Run YouTube analysis via MCP server.
        
        Args:
            video_url: YouTube video URL to analyze
            analysis_type: Type of analysis (full, captions, metadata, themes)
            
        Returns:
            JSON string with analysis results
        """
        
        # Placeholder implementation
        # In real implementation, this would call the MCP server
        placeholder_result = {
            "video_url": video_url,
            "analysis_type": analysis_type,
            "title": "Sample Video Title",
            "description": "Sample video description...",
            "duration": "10:30",
            "captions": "Sample transcript content...",
            "themes": ["adventure", "travel", "exploration"],
            "actionable_insights": [
                "Interest in outdoor activities",
                "Preference for guided experiences",
                "Focus on photography opportunities"
            ],
            "target_audience": "adventure seekers",
            "mood": "excited and adventurous"
        }
        
        return json.dumps(placeholder_result, indent=2)


class ExaMCPTool(BaseTool):
    """
    Tool for semantic search and local experience discovery via MCP server.
    Provides intelligent search capabilities for events and activities.
    """
    
    name: str = "exa_mcp"
    description: str = """
    Perform semantic search for local experiences and events.
    
    Capabilities:
    - Search for local events and activities
    - Find experiences matching specific themes
    - Discover venues and attractions
    - Get event details and availability
    """
    
    server_url: str = Field(default_factory=lambda: os.getenv("EXA_MCP_SERVER_URL", "http://localhost:8001/mcp"))
    api_key: str = Field(default_factory=lambda: os.getenv("EXA_API_KEY", ""))
    
    def _run(self, query: str, location: str, date: str = None, limit: int = 10) -> str:
        """
        Search for local experiences via MCP server.
        
        Args:
            query: Search query describing desired experiences
            location: Target location for search
            date: Optional target date
            limit: Maximum number of results
            
        Returns:
            JSON string with search results
        """
        
        # Placeholder implementation
        placeholder_result = {
            "query": query,
            "location": location,
            "date": date,
            "results": [
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
                    "booking_url": "https://example.com/book"
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
                    "booking_url": "https://example.com/book"
                }
            ]
        }
        
        return json.dumps(placeholder_result, indent=2)


class MapsMCPTool(BaseTool):
    """
    Tool for route planning and navigation via MCP server.
    Provides mapping and routing capabilities.
    """
    
    name: str = "maps_mcp"
    description: str = """
    Plan routes and get navigation information with shareable links.
    
    Capabilities:
    - Calculate optimal routes between locations
    - Get driving, walking, and transit directions
    - Generate shareable Google Maps links for calendar integration
    - Create complete itinerary routes with waypoints
    - Estimate travel times and distances
    - Find parking and accessibility information
    """
    
    server_url: str = Field(default_factory=lambda: os.getenv("MAPS_MCP_SERVER_URL", "http://localhost:8003/mcp"))
    api_key: str = Field(default_factory=lambda: os.getenv("GOOGLE_MAPS_API_KEY", ""))
    
    def _run(self, origin: str, destination: str, mode: str = "driving", 
             waypoints: List[str] = None) -> str:
        """
        Plan route via MCP server.
        
        Args:
            origin: Starting location
            destination: Destination location
            mode: Transportation mode (driving, walking, transit)
            waypoints: Optional waypoints to include
            
        Returns:
            JSON string with route information
        """
        
        try:
            # Prepare request data
            request_data = {
                "method": "directions",
                "args": {
                    "origin": origin,
                    "destination": destination,
                    "mode": mode,
                    "waypoints": waypoints or []
                }
            }
            
            # Call MCP server
            response = requests.post(
                f"{self.server_url}/run",
                json=request_data,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                return json.dumps(result["data"], indent=2)
            else:
                return json.dumps({
                    "error": result.get("error", "Unknown error"),
                    "fallback": True,
                    "message": "Using fallback data due to MCP server error"
                }, indent=2)
                
        except Exception as e:
            # Fallback to placeholder on error
            fallback_result = {
                "origin": origin,
                "destination": destination,
                "mode": mode,
                "waypoints": waypoints or [],
                "error": str(e),
                "fallback": True,
                "route": {
                    "distance": "Estimated 12.5 miles",
                    "duration": "Estimated 25 minutes",
                    "steps": [
                        {"instruction": "Route calculation failed - using estimated data", 
                         "distance": "N/A", "duration": "N/A"}
                    ]
                }
            }
            
            return json.dumps(fallback_result, indent=2)
    
    def generate_itinerary_route(self, experiences: List[Dict], start_location: str, 
                                mode: str = "driving", optimize: bool = True) -> str:
        """
        Generate a complete itinerary route with shareable links for calendar integration.
        
        Args:
            experiences: List of experience dictionaries with locations
            start_location: Starting location
            mode: Transportation mode (driving, walking, transit)
            optimize: Whether to optimize the route order
            
        Returns:
            JSON string with complete route information and shareable links
        """
        
        try:
            # Prepare request data
            request_data = {
                "method": "generate_itinerary_route",
                "args": {
                    "experiences": experiences,
                    "start_location": start_location,
                    "mode": mode,
                    "optimize": optimize
                }
            }
            
            # Call MCP server
            response = requests.post(
                f"{self.server_url}/run",
                json=request_data,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get("success"):
                return json.dumps(result["data"], indent=2)
            else:
                return json.dumps({
                    "error": result.get("error", "Unknown error"),
                    "fallback": True,
                    "message": "Failed to generate itinerary route"
                }, indent=2)
                
        except Exception as e:
            # Fallback to basic route info on error
            fallback_result = {
                "error": str(e),
                "fallback": True,
                "experiences": experiences,
                "start_location": start_location,
                "message": "Could not generate shareable links - using basic route info",
                "basic_route_link": f"https://www.google.com/maps/search/{start_location.replace(' ', '+')}"
            }
            
            return json.dumps(fallback_result, indent=2)


class CalendarMCPTool(BaseTool):
    """
    Tool for calendar management via MCP server.
    Provides calendar event creation and management.
    """
    
    name: str = "calendar_mcp"
    description: str = """
    Manage calendar events and invitations.
    
    Capabilities:
    - Create calendar events
    - Send invitations to participants
    - Check availability
    - Set reminders and notifications
    """
    
    server_url: str = Field(default_factory=lambda: os.getenv("CALENDAR_MCP_SERVER_URL", "http://localhost:8004/mcp"))
    api_key: str = Field(default_factory=lambda: os.getenv("GOOGLE_CALENDAR_API_KEY", ""))
    
    def _run(self, action: str, event_data: Dict[str, Any] = None, 
             participants: List[str] = None) -> str:
        """
        Manage calendar events via MCP server.
        
        Args:
            action: Action to perform (create, update, delete, invite)
            event_data: Event details dictionary
            participants: List of participant email addresses
            
        Returns:
            JSON string with operation results
        """
        
        # Placeholder implementation
        placeholder_result = {
            "action": action,
            "event_data": event_data or {},
            "participants": participants or [],
            "result": {
                "success": True,
                "event_id": "evt_123456789",
                "calendar_url": "https://calendar.google.com/event?eid=123456789",
                "invitations_sent": len(participants) if participants else 0,
                "created_at": "2024-01-15T10:00:00Z"
            }
        }
        
        return json.dumps(placeholder_result, indent=2)


class TTSMCPTool(BaseTool):
    """
    Tool for text-to-speech conversion via MCP server.
    Provides high-quality audio generation capabilities.
    """
    
    name: str = "tts_mcp"
    description: str = """
    Convert text to high-quality speech audio.
    
    Capabilities:
    - Generate natural-sounding speech
    - Multiple voice options and styles
    - Adjust speech rate and pitch
    - Export in various audio formats
    """
    
    server_url: str = Field(default_factory=lambda: os.getenv("TTS_MCP_SERVER_URL", "http://localhost:8005/mcp"))
    api_key: str = Field(default_factory=lambda: os.getenv("ELEVENLABS_API_KEY", ""))
    
    def _run(self, text: str, voice: str = "default", settings: Dict[str, Any] = None) -> str:
        """
        Convert text to speech via MCP server.
        
        Args:
            text: Text to convert to speech
            voice: Voice ID or name to use
            settings: Voice settings (rate, pitch, etc.)
            
        Returns:
            JSON string with audio generation results
        """
        
        # Placeholder implementation
        placeholder_result = {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "voice": voice,
            "settings": settings or {},
            "result": {
                "success": True,
                "audio_url": "https://storage.example.com/audio/generated_audio_123.mp3",
                "duration": "2:30",
                "file_size": "2.1 MB",
                "format": "mp3",
                "quality": "high",
                "generated_at": "2024-01-15T10:30:00Z"
            }
        }
        
        return json.dumps(placeholder_result, indent=2)


# Export all tools for easy importing
__all__ = [
    "YouTubeMCPTool",
    "ExaMCPTool",
    "MapsMCPTool",
    "CalendarMCPTool",
    "TTSMCPTool"
]


# Example usage and testing
if __name__ == "__main__":
    # Test YouTube tool
    youtube_tool = YouTubeMCPTool()
    result = youtube_tool._run("https://youtube.com/watch?v=example", "full")
    print("YouTube Tool Result:")
    print(result)
    
    # Test Exa tool
    exa_tool = ExaMCPTool()
    result = exa_tool._run("adventure photography", "San Francisco, CA", "2024-01-15")
    print("\nExa Tool Result:")
    print(result) 