"""
Maps MCP Tool Wrapper

Thin wrapper for Google Maps MCP server calls.
"""

import os
import requests
from crewai.tools import tool
from typing import Dict, Any, List

BASE_URL = os.getenv("MAPS_MCP_URL", "http://localhost:8002")

@tool("maps.route")
def maps_route(origin: str, destination: str, mode: str = "driving") -> Dict[str, Any]:
    """Get route between two locations."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "route",
                "args": {
                    "origin": origin,
                    "destination": destination,
                    "mode": mode
                }
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # Fallback data for testing
        return {
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "distance": "Estimated 5.3 miles",
            "duration": "Estimated 15 minutes",
            "steps": [
                {
                    "instruction": "Route calculation failed - using estimated data",
                    "distance": "N/A",
                    "duration": "N/A"
                }
            ],
            "error": str(e),
            "fallback": True
        }

@tool("maps.generate_shareable_link")
def maps_generate_shareable_link(origin: str, destination: str, waypoints: List[str] = None) -> str:
    """Generate shareable Google Maps link for navigation."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "generate_shareable_link",
                "args": {
                    "origin": origin,
                    "destination": destination,
                    "waypoints": waypoints or []
                }
            },
            timeout=15
        )
        response.raise_for_status()
        return response.json().get("url", "")
    except Exception as e:
        # Generate fallback link
        encoded_origin = origin.replace(" ", "+").replace(",", "%2C")
        encoded_dest = destination.replace(" ", "+").replace(",", "%2C")
        return f"https://www.google.com/maps/dir/{encoded_origin}/{encoded_dest}/"

@tool("maps.itinerary_route")
def maps_itinerary_route(origin: str, destinations: List[str], mode: str = "driving") -> Dict[str, Any]:
    """Generate complete itinerary route with shareable links."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "generate_itinerary_route",
                "args": {
                    "origin": origin,
                    "destinations": destinations,
                    "mode": mode
                }
            },
            timeout=45
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # Fallback route generation
        legs = []
        total_distance = 0
        total_duration = 0
        
        current_location = origin
        for i, dest in enumerate(destinations):
            leg_data = maps_route(current_location, dest, mode)
            
            # Extract numeric values for totals (simplified)
            distance_val = 5.0 + i * 2.0  # Estimated
            duration_val = 15 + i * 8     # Estimated
            
            legs.append({
                "origin": current_location,
                "destination": dest,
                "distance": f"{distance_val} miles",
                "duration": f"{duration_val} mins",
                "shareable_link": maps_generate_shareable_link(current_location, dest)
            })
            
            total_distance += distance_val
            total_duration += duration_val
            current_location = dest
        
        return {
            "origin": origin,
            "destinations": destinations,
            "mode": mode,
            "total_distance": f"{total_distance:.1f} miles",
            "total_duration": f"{total_duration} mins",
            "legs": legs,
            "complete_route_link": maps_generate_shareable_link(origin, destinations[-1], destinations[:-1]),
            "error": str(e),
            "fallback": True
        }