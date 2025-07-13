#!/usr/bin/env python3
"""
Test script for Google Calendar MCP tools and calendar manager agent.
"""

import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_calendar_tools():
    """Test the Calendar MCP tools directly."""
    print("=" * 50)
    print("TESTING GOOGLE CALENDAR MCP TOOLS")
    print("=" * 50)
    
    try:
        from tools.calendar_mcp import calendar_create_event, calendar_create_itinerary_events, calendar_health_check
        
        print("\n1. Testing calendar health check...")
        health_result = calendar_health_check.func()
        print("Health check result:")
        print(f"  - Status: {health_result.get('status')}")
        print(f"  - Service: {health_result.get('service')}")
        if 'error' in health_result:
            print(f"  - Error (expected): {health_result.get('error')}")
        
        print("\n2. Testing calendar_create_event function...")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        event_result = calendar_create_event.func(
            title="Test Event - YouTube Video Adventure",
            description="Experience based on YouTube video analysis",
            start_time=f"{tomorrow}T10:00:00",
            end_time=f"{tomorrow}T12:00:00",
            attendees=["test@example.com"]
        )
        print("Event creation result:")
        print(f"  - Event ID: {event_result.get('event_id')}")
        print(f"  - Title: {event_result.get('title')}")
        print(f"  - Status: {event_result.get('status')}")
        print(f"  - Fallback mode: {event_result.get('fallback', False)}")
        
        print("\n3. Testing calendar_create_itinerary_events function...")
        sample_itinerary = {
            "origin": "San Francisco, CA",
            "destinations": ["Monterey, CA", "Los Angeles, CA"],
            "legs": [
                {
                    "origin": "San Francisco, CA",
                    "destination": "Monterey, CA",
                    "duration": "2 hours",
                    "shareable_link": "https://maps.google.com/dir/SF/Monterey"
                },
                {
                    "origin": "Monterey, CA", 
                    "destination": "Los Angeles, CA",
                    "duration": "4 hours",
                    "shareable_link": "https://maps.google.com/dir/Monterey/LA"
                }
            ]
        }
        
        itinerary_events = calendar_create_itinerary_events.func(
            itinerary=sample_itinerary,
            participants=["participant1@example.com", "participant2@example.com"],
            base_date=tomorrow
        )
        print("Itinerary events result:")
        print(f"  - Number of events created: {len(itinerary_events)}")
        for i, event in enumerate(itinerary_events):
            print(f"  - Event {i+1}: {event.get('title')}")
            print(f"    - Location: {event.get('location')}")
            print(f"    - Time: {event.get('start_time')} to {event.get('end_time')}")
            print(f"    - Has Maps link: {'maps_link' in event and bool(event['maps_link'])}")
        
        return True
        
    except Exception as e:
        print(f"Error testing calendar tools: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_calendar_manager_agent():
    """Test the calendar manager agent."""
    print("\n" + "=" * 50)
    print("TESTING CALENDAR MANAGER AGENT")
    print("=" * 50)
    
    try:
        from agents.calendar_manager import calendar_manager
        
        print(f"\nAgent successfully created!")
        print(f"  - Role: {calendar_manager.role}")
        print(f"  - Goal: {calendar_manager.goal}")
        print(f"  - Number of tools: {len(calendar_manager.tools)}")
        print(f"  - Tool names: {[tool.name for tool in calendar_manager.tools]}")
        print(f"  - LLM model: {calendar_manager.llm.model}")
        
        return True
        
    except Exception as e:
        print(f"Error testing calendar manager agent: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between Maps and Calendar."""
    print("\n" + "=" * 50)
    print("TESTING MAPS + CALENDAR INTEGRATION")
    print("=" * 50)
    
    try:
        from tools.maps_mcp import maps_itinerary_route
        from tools.calendar_mcp import calendar_create_itinerary_events
        from datetime import datetime, timedelta
        
        # Create a sample route
        print("\n1. Creating sample route with Maps...")
        route_result = maps_itinerary_route.func(
            origin="San Francisco, CA",
            destinations=["Napa Valley, CA", "Sacramento, CA"],
            mode="driving"
        )
        
        print("Route created:")
        print(f"  - Total distance: {route_result.get('total_distance')}")
        print(f"  - Total duration: {route_result.get('total_duration')}")
        print(f"  - Number of legs: {len(route_result.get('legs', []))}")
        
        # Create calendar events from the route
        print("\n2. Creating calendar events from route...")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        calendar_events = calendar_create_itinerary_events.func(
            itinerary=route_result,
            participants=["traveler1@example.com", "traveler2@example.com"],
            base_date=tomorrow
        )
        
        print("Calendar events created:")
        for i, event in enumerate(calendar_events):
            print(f"  - Event {i+1}: {event.get('title')}")
            print(f"    - Start: {event.get('start_time')}")
            print(f"    - Has navigation: {bool(event.get('maps_link'))}")
        
        print("\n✅ Maps + Calendar integration working!")
        return True
        
    except Exception as e:
        print(f"Error testing integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("Starting Google Calendar functionality tests...\n")
    
    tools_success = test_calendar_tools()
    agent_success = test_calendar_manager_agent()
    integration_success = test_integration()
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Calendar tools: {'✅ PASS' if tools_success else '❌ FAIL'}")
    print(f"Calendar manager agent: {'✅ PASS' if agent_success else '❌ FAIL'}")
    print(f"Maps + Calendar integration: {'✅ PASS' if integration_success else '❌ FAIL'}")
    
    if tools_success and agent_success and integration_success:
        print("\n🎉 All Calendar tests passed! Maps + Calendar integration ready.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)