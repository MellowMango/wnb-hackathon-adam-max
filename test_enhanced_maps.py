#!/usr/bin/env python3
"""
Test enhanced Google Maps MCP with shareable links for calendar integration
"""

import json
import requests
from tools.mcp_tools import MapsMCPTool

def test_itinerary_route_generation():
    """Test the new itinerary route generation with shareable links"""
    print("🗺️  Testing Enhanced Google Maps MCP with shareable links...")
    
    try:
        # Test data: San Francisco itinerary
        experiences = [
            {
                "name": "Golden Gate Bridge Visit",
                "location": "Golden Gate Bridge, San Francisco, CA",
                "description": "Iconic bridge viewing and photography"
            },
            {
                "name": "Alcatraz Island Tour", 
                "location": "Alcatraz Island, San Francisco, CA",
                "description": "Historic prison tour"
            },
            {
                "name": "Fisherman's Wharf",
                "location": "Fisherman's Wharf, San Francisco, CA", 
                "description": "Waterfront dining and shopping"
            }
        ]
        
        start_location = "Union Square, San Francisco, CA"
        
        # Test direct MCP server call
        print("🧪 Testing direct MCP server call...")
        request_data = {
            "method": "generate_itinerary_route",
            "args": {
                "experiences": experiences,
                "start_location": start_location,
                "mode": "driving",
                "optimize": True
            }
        }
        
        response = requests.post(
            "http://localhost:8003/mcp/run",
            json=request_data,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        if result.get("success"):
            data = result["data"]
            print(f"✅ Itinerary route generated successfully!")
            print(f"📍 Total experiences: {data['experience_count']}")
            print(f"📏 Total distance: {data['total_distance']}")
            print(f"⏱️  Total duration: {data['total_duration']}")
            print(f"🔗 Complete route link: {data['complete_route_link']}")
            
            print(f"\n📋 Individual legs with shareable links:")
            for i, leg in enumerate(data['legs']):
                print(f"  {i+1}. {leg['experience_name']}")
                print(f"     Distance: {leg.get('distance', 'N/A')}")
                print(f"     Duration: {leg.get('duration', 'N/A')}")
                print(f"     Link: {leg['shareable_link']}")
                print(f"     Calendar desc: {leg['calendar_description'][:100]}...")
                print()
            
        else:
            print(f"❌ MCP server error: {result.get('error')}")
            return False
        
        # Test CrewAI tool integration
        print("🧪 Testing CrewAI MapsMCPTool integration...")
        maps_tool = MapsMCPTool()
        
        tool_result = maps_tool.generate_itinerary_route(
            experiences=experiences,
            start_location=start_location,
            mode="driving",
            optimize=True
        )
        
        tool_data = json.loads(tool_result)
        if not tool_data.get("error"):
            print(f"✅ CrewAI tool integration working!")
            print(f"🔗 Tool generated complete route: {tool_data.get('complete_route_link', 'Not found')}")
        else:
            print(f"❌ CrewAI tool error: {tool_data.get('error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 Testing Enhanced Google Maps MCP for Calendar Integration")
    print("=" * 60)
    
    success = test_itinerary_route_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! Maps MCP now generates shareable links for calendar integration!")
        print("📅 Calendar agents can now include Google Maps links in event descriptions")
    else:
        print("❌ Some tests failed - check logs above")