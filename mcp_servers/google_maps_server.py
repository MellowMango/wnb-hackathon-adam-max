#!/usr/bin/env python3
"""
Google Maps MCP Server

FastAPI-based Model Context Protocol server for Google Maps API integration.
Provides geocoding, place search, directions, and distance matrix functionality.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import googlemaps
import asyncio
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Google Maps MCP Server",
    description="Model Context Protocol server for Google Maps API",
    version="1.0.0"
)

# Initialize Google Maps client
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not GOOGLE_MAPS_API_KEY:
    logger.warning("GOOGLE_MAPS_API_KEY not found - server will not function properly")
    gmaps = None
else:
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    logger.info("Google Maps client initialized successfully")


class MCPRequest(BaseModel):
    """Standard MCP request format"""
    method: str
    args: Dict[str, Any]


class MCPResponse(BaseModel):
    """Standard MCP response format"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "google-maps-mcp",
        "timestamp": datetime.now().isoformat(),
        "maps_client": "initialized" if gmaps else "not_initialized"
    }


@app.post("/mcp/run")
async def run_mcp_method(request: MCPRequest) -> MCPResponse:
    """
    Main MCP endpoint that routes requests to appropriate Google Maps functions.
    
    Supported methods:
    - geocode: Convert address to coordinates
    - reverse_geocode: Convert coordinates to address  
    - search_places: Search for places
    - place_details: Get detailed place information
    - directions: Get routing directions
    - distance_matrix: Calculate travel distances and times
    - elevation: Get elevation data
    """
    
    if not gmaps:
        return MCPResponse(
            success=False,
            error="Google Maps client not initialized - check API key"
        )
    
    try:
        method = request.method
        args = request.args
        
        if method == "geocode":
            result = await handle_geocode(args)
        elif method == "reverse_geocode":
            result = await handle_reverse_geocode(args)
        elif method == "search_places":
            result = await handle_search_places(args)
        elif method == "place_details":
            result = await handle_place_details(args)
        elif method == "directions":
            result = await handle_directions(args)
        elif method == "distance_matrix":
            result = await handle_distance_matrix(args)
        elif method == "elevation":
            result = await handle_elevation(args)
        elif method == "generate_itinerary_route":
            result = await handle_generate_itinerary_route(args)
        else:
            return MCPResponse(
                success=False,
                error=f"Unknown method: {method}"
            )
        
        return MCPResponse(success=True, data=result)
        
    except Exception as e:
        logger.error(f"Error processing MCP request: {e}")
        return MCPResponse(
            success=False,
            error=str(e)
        )


async def handle_geocode(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert address to coordinates.
    
    Args:
        address: Address string to geocode
        
    Returns:
        Dictionary with coordinates and formatted address
    """
    address = args.get("address")
    if not address:
        raise ValueError("address parameter is required")
    
    result = gmaps.geocode(address)
    
    if not result:
        return {"found": False, "message": "No results found"}
    
    location = result[0]
    
    return {
        "found": True,
        "latitude": location["geometry"]["location"]["lat"],
        "longitude": location["geometry"]["location"]["lng"],
        "formatted_address": location["formatted_address"],
        "place_id": location["place_id"],
        "types": location["types"],
        "address_components": location["address_components"]
    }


async def handle_reverse_geocode(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert coordinates to address.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        Dictionary with address information
    """
    latitude = args.get("latitude")
    longitude = args.get("longitude")
    
    if latitude is None or longitude is None:
        raise ValueError("latitude and longitude parameters are required")
    
    result = gmaps.reverse_geocode((latitude, longitude))
    
    if not result:
        return {"found": False, "message": "No address found for coordinates"}
    
    location = result[0]
    
    return {
        "found": True,
        "formatted_address": location["formatted_address"],
        "place_id": location["place_id"],
        "types": location["types"],
        "address_components": location["address_components"]
    }


async def handle_search_places(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Search for places using text query.
    
    Args:
        query: Search query string
        location: Optional location bias (latitude, longitude)
        radius: Optional search radius in meters
        type: Optional place type filter
        
    Returns:
        Dictionary with search results
    """
    query = args.get("query")
    if not query:
        raise ValueError("query parameter is required")
    
    location = args.get("location")
    radius = args.get("radius", 5000)  # Default 5km radius
    place_type = args.get("type")
    
    # Use places_nearby if location provided, otherwise text search
    if location:
        if isinstance(location, str):
            # Convert address to coordinates first
            geocode_result = gmaps.geocode(location)
            if geocode_result:
                location = geocode_result[0]["geometry"]["location"]
            else:
                raise ValueError(f"Could not geocode location: {location}")
        elif isinstance(location, (list, tuple)) and len(location) == 2:
            location = {"lat": location[0], "lng": location[1]}
        
        result = gmaps.places_nearby(
            location=location,
            radius=radius,
            keyword=query,
            type=place_type
        )
    else:
        result = gmaps.places(query=query, type=place_type)
    
    places = []
    for place in result.get("results", []):
        place_info = {
            "name": place.get("name"),
            "place_id": place.get("place_id"),
            "formatted_address": place.get("vicinity") or place.get("formatted_address"),
            "rating": place.get("rating"),
            "user_ratings_total": place.get("user_ratings_total"),
            "price_level": place.get("price_level"),
            "types": place.get("types", []),
            "geometry": place.get("geometry"),
            "photos": [{"photo_reference": photo.get("photo_reference")} 
                      for photo in place.get("photos", [])]
        }
        places.append(place_info)
    
    return {
        "places": places,
        "count": len(places),
        "status": result.get("status")
    }


async def handle_place_details(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get detailed information about a specific place.
    
    Args:
        place_id: Google Place ID
        fields: Optional list of fields to retrieve
        
    Returns:
        Dictionary with detailed place information
    """
    place_id = args.get("place_id")
    if not place_id:
        raise ValueError("place_id parameter is required")
    
    fields = args.get("fields", [
        "name", "formatted_address", "geometry", "rating", 
        "user_ratings_total", "price_level", "opening_hours",
        "phone_number", "website", "reviews", "photos", "types"
    ])
    
    result = gmaps.place(place_id=place_id, fields=fields)
    
    if result["status"] != "OK":
        return {"found": False, "status": result["status"]}
    
    place = result["result"]
    
    return {
        "found": True,
        "place_id": place_id,
        "name": place.get("name"),
        "formatted_address": place.get("formatted_address"),
        "geometry": place.get("geometry"),
        "rating": place.get("rating"),
        "user_ratings_total": place.get("user_ratings_total"),
        "price_level": place.get("price_level"),
        "opening_hours": place.get("opening_hours"),
        "phone_number": place.get("formatted_phone_number"),
        "website": place.get("website"),
        "types": place.get("types", []),
        "reviews": place.get("reviews", []),
        "photos": [{"photo_reference": photo.get("photo_reference")} 
                  for photo in place.get("photos", [])]
    }


async def handle_directions(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get routing directions between locations.
    
    Args:
        origin: Starting location (address or coordinates)
        destination: Ending location (address or coordinates)
        mode: Travel mode (driving, walking, bicycling, transit)
        waypoints: Optional intermediate waypoints
        optimize_waypoints: Whether to optimize waypoint order
        avoid: Optional route restrictions (tolls, highways, ferries, indoor)
        departure_time: Optional departure time for transit
        
    Returns:
        Dictionary with route information
    """
    origin = args.get("origin")
    destination = args.get("destination")
    
    if not origin or not destination:
        raise ValueError("origin and destination parameters are required")
    
    mode = args.get("mode", "driving")
    waypoints = args.get("waypoints", [])
    optimize_waypoints = args.get("optimize_waypoints", False)
    avoid = args.get("avoid", [])
    departure_time = args.get("departure_time")
    
    if departure_time and isinstance(departure_time, str):
        departure_time = datetime.fromisoformat(departure_time)
    
    result = gmaps.directions(
        origin=origin,
        destination=destination,
        mode=mode,
        waypoints=waypoints,
        optimize_waypoints=optimize_waypoints,
        avoid=avoid,
        departure_time=departure_time
    )
    
    if not result:
        return {"found": False, "message": "No routes found"}
    
    route = result[0]  # Take first route
    leg = route["legs"][0]  # Take first leg
    
    # Generate shareable Google Maps links
    def generate_shareable_link(origin, destination, waypoints=None, mode="driving"):
        """Generate a shareable Google Maps link"""
        base_url = "https://www.google.com/maps/dir/"
        
        # Build the URL with origin, waypoints, and destination
        locations = [origin]
        if waypoints:
            locations.extend(waypoints)
        locations.append(destination)
        
        # URL encode the locations
        import urllib.parse
        encoded_locations = [urllib.parse.quote_plus(loc) for loc in locations]
        
        # Build the complete URL
        maps_url = base_url + "/".join(encoded_locations)
        
        # Add travel mode parameter
        mode_mapping = {
            "driving": "driving",
            "walking": "walking", 
            "bicycling": "bicycling",
            "transit": "transit"
        }
        maps_url += f"/@?entry=ttu&g_ep=EgoyMDI0MTIwMy4wIKXMDSoASAFQAw%3D%3D&mode={mode_mapping.get(mode, 'driving')}"
        
        return maps_url
    
    # Generate the shareable link
    shareable_link = generate_shareable_link(
        origin=origin,
        destination=destination, 
        waypoints=waypoints,
        mode=mode
    )
    
    # Generate calendar-friendly summary
    calendar_summary = f"{leg['start_address']} → {leg['end_address']}"
    if waypoints:
        calendar_summary = f"Multi-stop route: {len(waypoints + 2)} locations"
    
    return {
        "found": True,
        "summary": route.get("summary"),
        "distance": leg["distance"]["text"],
        "duration": leg["duration"]["text"],
        "distance_value": leg["distance"]["value"],
        "duration_value": leg["duration"]["value"],
        "start_address": leg["start_address"],
        "end_address": leg["end_address"],
        "steps": [
            {
                "instruction": step["html_instructions"],
                "distance": step["distance"]["text"],
                "duration": step["duration"]["text"],
                "start_location": step["start_location"],
                "end_location": step["end_location"]
            }
            for step in leg["steps"]
        ],
        "overview_polyline": route["overview_polyline"]["points"],
        "warnings": route.get("warnings", []),
        "waypoint_order": route.get("waypoint_order", []),
        # NEW: Shareable links for calendar integration
        "shareable_link": shareable_link,
        "calendar_summary": calendar_summary,
        "calendar_description": f"Route: {calendar_summary}\nDistance: {leg['distance']['text']}\nDuration: {leg['duration']['text']}\nView route: {shareable_link}"
    }


async def handle_distance_matrix(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate distance and travel time between multiple origins and destinations.
    
    Args:
        origins: List of origin locations
        destinations: List of destination locations
        mode: Travel mode (driving, walking, bicycling, transit)
        avoid: Optional route restrictions
        units: Distance units (metric, imperial)
        
    Returns:
        Dictionary with distance matrix
    """
    origins = args.get("origins", [])
    destinations = args.get("destinations", [])
    
    if not origins or not destinations:
        raise ValueError("origins and destinations parameters are required")
    
    mode = args.get("mode", "driving")
    avoid = args.get("avoid", [])
    units = args.get("units", "metric")
    
    result = gmaps.distance_matrix(
        origins=origins,
        destinations=destinations,
        mode=mode,
        avoid=avoid,
        units=units
    )
    
    if result["status"] != "OK":
        return {"success": False, "status": result["status"]}
    
    return {
        "success": True,
        "origin_addresses": result["origin_addresses"],
        "destination_addresses": result["destination_addresses"],
        "rows": result["rows"]
    }


async def handle_elevation(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get elevation data for specified locations.
    
    Args:
        locations: List of locations (coordinates)
        
    Returns:
        Dictionary with elevation data
    """
    locations = args.get("locations", [])
    
    if not locations:
        raise ValueError("locations parameter is required")
    
    result = gmaps.elevation(locations)
    
    return {
        "results": [
            {
                "elevation": point["elevation"],
                "location": point["location"],
                "resolution": point["resolution"]
            }
            for point in result
        ],
        "count": len(result)
    }


async def handle_generate_itinerary_route(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a complete itinerary route with shareable links for calendar integration.
    
    Args:
        experiences: List of experience locations to visit
        start_location: Starting location
        mode: Travel mode
        optimize: Whether to optimize the route order
        
    Returns:
        Dictionary with optimized route and shareable links for each segment
    """
    experiences = args.get("experiences", [])
    start_location = args.get("start_location")
    mode = args.get("mode", "driving")
    optimize = args.get("optimize", True)
    
    if not experiences or not start_location:
        raise ValueError("experiences and start_location parameters are required")
    
    # Extract locations from experiences
    waypoints = []
    experience_names = []
    
    for exp in experiences:
        if isinstance(exp, dict):
            location = exp.get("location") or exp.get("address") or exp.get("name")
            name = exp.get("name", location)
        else:
            location = str(exp)
            name = location
        
        if location:
            waypoints.append(location)
            experience_names.append(name)
    
    if not waypoints:
        raise ValueError("No valid locations found in experiences")
    
    # Get the optimized route through all locations
    result = gmaps.directions(
        origin=start_location,
        destination=waypoints[-1],  # End at last location
        waypoints=waypoints[:-1] if len(waypoints) > 1 else None,
        optimize_waypoints=optimize,
        mode=mode
    )
    
    if not result:
        return {"found": False, "message": "No route found"}
    
    route = result[0]
    
    # Generate shareable link for complete route
    import urllib.parse
    base_url = "https://www.google.com/maps/dir/"
    all_locations = [start_location] + waypoints
    encoded_locations = [urllib.parse.quote_plus(loc) for loc in all_locations]
    complete_route_link = base_url + "/".join(encoded_locations)
    
    # Add mode parameter
    mode_mapping = {
        "driving": "driving",
        "walking": "walking", 
        "bicycling": "bicycling",
        "transit": "transit"
    }
    complete_route_link += f"/@?entry=ttu&g_ep=EgoyMDI0MTIwMy4wIKXMDSoASAFQAw%3D%3D&mode={mode_mapping.get(mode, 'driving')}"
    
    # Generate individual leg information with shareable links
    legs_info = []
    current_origin = start_location
    
    for i, (waypoint, name) in enumerate(zip(waypoints, experience_names)):
        # Generate individual leg link
        leg_link = f"https://www.google.com/maps/dir/{urllib.parse.quote_plus(current_origin)}/{urllib.parse.quote_plus(waypoint)}/@?entry=ttu&mode={mode_mapping.get(mode, 'driving')}"
        
        # Get leg details from route
        if i < len(route["legs"]):
            leg = route["legs"][i]
            legs_info.append({
                "experience_name": name,
                "origin": current_origin,
                "destination": waypoint,
                "distance": leg["distance"]["text"],
                "duration": leg["duration"]["text"],
                "distance_value": leg["distance"]["value"],
                "duration_value": leg["duration"]["value"],
                "shareable_link": leg_link,
                "calendar_description": f"Travel to {name}\nFrom: {current_origin}\nTo: {waypoint}\nDistance: {leg['distance']['text']}\nDuration: {leg['duration']['text']}\nDirections: {leg_link}"
            })
        else:
            # Fallback for missing leg data
            legs_info.append({
                "experience_name": name,
                "origin": current_origin,
                "destination": waypoint,
                "shareable_link": leg_link,
                "calendar_description": f"Travel to {name}\nDirections: {leg_link}"
            })
        
        current_origin = waypoint
    
    # Calculate total stats
    total_distance = sum(leg["distance"]["value"] for leg in route["legs"])
    total_duration = sum(leg["duration"]["value"] for leg in route["legs"])
    
    # Convert totals to readable format
    total_distance_text = f"{total_distance / 1609.34:.1f} miles" if total_distance > 1609 else f"{total_distance} meters"
    total_duration_text = f"{total_duration // 3600}h {(total_duration % 3600) // 60}m" if total_duration >= 3600 else f"{total_duration // 60}m"
    
    return {
        "found": True,
        "itinerary_summary": f"{len(experiences)} experiences planned",
        "total_distance": total_distance_text,
        "total_duration": total_duration_text,
        "total_distance_value": total_distance,
        "total_duration_value": total_duration,
        "start_location": start_location,
        "end_location": waypoints[-1],
        "experience_count": len(experiences),
        "legs": legs_info,
        "complete_route_link": complete_route_link,
        "optimized_order": route.get("waypoint_order", []),
        "calendar_master_description": f"Complete Itinerary Route\n{len(experiences)} experiences\nTotal distance: {total_distance_text}\nTotal duration: {total_duration_text}\nView complete route: {complete_route_link}",
        "overview_polyline": route["overview_polyline"]["points"]
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("MAPS_MCP_PORT", 8003))
    
    print(f"🗺️  Starting Google Maps MCP Server on port {port}")
    print(f"📍 Google Maps API Key: {'✅ Configured' if GOOGLE_MAPS_API_KEY else '❌ Missing'}")
    print(f"🔧 Health check: http://localhost:{port}/health")
    print(f"🚀 MCP endpoint: http://localhost:{port}/mcp/run")
    
    uvicorn.run(
        "google_maps_server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )