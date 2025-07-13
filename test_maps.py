#!/usr/bin/env python3
"""
Test script for Google Maps MCP tools and route planner agent.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_maps_tools():
    """Test the Maps MCP tools directly."""
    print("=" * 50)
    print("TESTING GOOGLE MAPS MCP TOOLS")
    print("=" * 50)
    
    try:
        from tools.maps_mcp import maps_route, maps_generate_shareable_link, maps_itinerary_route
        
        print("\n1. Testing maps_route function...")
        route_result = maps_route.func('San Francisco, CA', 'Los Angeles, CA', 'driving')
        print("Route result:")
        print(f"  - Origin: {route_result.get('origin')}")
        print(f"  - Destination: {route_result.get('destination')}")
        print(f"  - Distance: {route_result.get('distance')}")
        print(f"  - Duration: {route_result.get('duration')}")
        print(f"  - Fallback mode: {route_result.get('fallback', False)}")
        
        print("\n2. Testing maps_generate_shareable_link function...")
        link_result = maps_generate_shareable_link.func('San Francisco, CA', 'Los Angeles, CA')
        print(f"Shareable link: {link_result}")
        
        print("\n3. Testing maps_itinerary_route function...")
        itinerary_result = maps_itinerary_route.func(
            'San Francisco, CA', 
            ['Monterey, CA', 'San Luis Obispo, CA', 'Los Angeles, CA'], 
            'driving'
        )
        print("Itinerary result:")
        print(f"  - Total distance: {itinerary_result.get('total_distance')}")
        print(f"  - Total duration: {itinerary_result.get('total_duration')}")
        print(f"  - Number of legs: {len(itinerary_result.get('legs', []))}")
        print(f"  - Fallback mode: {itinerary_result.get('fallback', False)}")
        
        return True
        
    except Exception as e:
        print(f"Error testing maps tools: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_route_planner_agent():
    """Test the route planner agent."""
    print("\n" + "=" * 50)
    print("TESTING ROUTE PLANNER AGENT")
    print("=" * 50)
    
    try:
        from agents.route_planner import route_planner
        
        print(f"\nAgent successfully created!")
        print(f"  - Role: {route_planner.role}")
        print(f"  - Goal: {route_planner.goal}")
        print(f"  - Number of tools: {len(route_planner.tools)}")
        print(f"  - Tool names: {[tool.name for tool in route_planner.tools]}")
        print(f"  - LLM model: {route_planner.llm.model}")
        
        return True
        
    except Exception as e:
        print(f"Error testing route planner agent: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("Starting Google Maps functionality tests...\n")
    
    tools_success = test_maps_tools()
    agent_success = test_route_planner_agent()
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Maps tools: {'✅ PASS' if tools_success else '❌ FAIL'}")
    print(f"Route planner agent: {'✅ PASS' if agent_success else '❌ FAIL'}")
    
    if tools_success and agent_success:
        print("\n🎉 All Google Maps tests passed! Ready to proceed with Calendar integration.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)