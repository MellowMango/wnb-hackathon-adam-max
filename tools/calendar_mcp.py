"""
Calendar MCP Tool Wrapper

Thin wrapper for Google Calendar MCP server calls.
"""

import os
import requests
from crewai.tools import tool
from typing import Dict, Any, List
from datetime import datetime, timedelta

BASE_URL = os.getenv("CALENDAR_MCP_URL", "http://localhost:8003")

@tool("calendar.create_event")
def calendar_create_event(
    title: str,
    description: str,
    start_time: str,
    end_time: str,
    attendees: List[str] = None
) -> Dict[str, Any]:
    """Create a calendar event."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "create_event",
                "args": {
                    "title": title,
                    "description": description,
                    "start_time": start_time,
                    "end_time": end_time,
                    "attendees": attendees or []
                }
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "event_id": f"fallback_{datetime.now().timestamp()}",
            "title": title,
            "description": description,
            "start_time": start_time,
            "end_time": end_time,
            "attendees": attendees or [],
            "status": "created_fallback",
            "error": str(e),
            "fallback": True
        }

@tool("calendar.create_itinerary_events")
def calendar_create_itinerary_events(
    itinerary: Dict[str, Any],
    participants: List[str],
    base_date: str
) -> List[Dict[str, Any]]:
    """Create multiple calendar events for an itinerary."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "create_itinerary_events",
                "args": {
                    "itinerary": itinerary,
                    "participants": participants,
                    "base_date": base_date
                }
            },
            timeout=45
        )
        response.raise_for_status()
        return response.json().get("events", [])
    except Exception as e:
        # Create fallback events
        events = []
        
        # Extract activities from itinerary
        activities = []
        if isinstance(itinerary, dict):
            activities = itinerary.get("activities", [])
            if not activities and "legs" in itinerary:
                # Convert route legs to activities
                for leg in itinerary["legs"]:
                    activities.append({
                        "name": f"Travel to {leg.get('destination', 'destination')}",
                        "location": leg.get("destination", ""),
                        "duration": leg.get("duration", "30 mins"),
                        "description": f"Navigate to {leg.get('destination', '')}",
                        "maps_link": leg.get("shareable_link", "")
                    })
        
        # Create events for each activity
        for i, activity in enumerate(activities):
            start_hour = 9 + i * 2  # Start at 9 AM, 2 hours apart
            
            events.append({
                "event_id": f"fallback_event_{i}_{datetime.now().timestamp()}",
                "title": activity.get("name", f"Activity {i+1}"),
                "description": f"{activity.get('description', '')}\n\nNavigation: {activity.get('maps_link', 'N/A')}",
                "start_time": f"{base_date}T{start_hour:02d}:00:00",
                "end_time": f"{base_date}T{start_hour+1:02d}:30:00",
                "location": activity.get("location", ""),
                "attendees": participants,
                "maps_link": activity.get("maps_link", ""),
                "status": "created_fallback",
                "error": str(e),
                "fallback": True
            })
        
        return events

@tool("calendar.health_check")
def calendar_health_check() -> Dict[str, Any]:
    """Check if calendar service is healthy."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        response.raise_for_status()
        return {"status": "healthy", "service": "calendar"}
    except Exception as e:
        return {"status": "unhealthy", "service": "calendar", "error": str(e)}