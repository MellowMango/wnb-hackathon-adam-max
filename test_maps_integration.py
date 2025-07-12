#!/usr/bin/env python3
"""
Test Google Maps MCP integration
"""

import os
import json
import requests
from tools.mcp_tools import MapsMCPTool

def test_direct_mcp_call():
    """Test direct MCP server call"""
    print("🧪 Testing direct Google Maps MCP server call...")
    
    try:
        # Test geocoding
        request_data = {
            "method": "geocode",
            "args": {
                "address": "Golden Gate Bridge, San Francisco, CA"
            }
        }
        
        response = requests.post(
            "http://localhost:8003/mcp/run",
            json=request_data,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ Geocoding result: {json.dumps(result, indent=2)}")
        
        # Test directions
        request_data = {
            "method": "directions",
            "args": {
                "origin": "Golden Gate Bridge, San Francisco, CA",
                "destination": "Alcatraz Island, San Francisco, CA",
                "mode": "driving"
            }
        }
        
        response = requests.post(
            "http://localhost:8003/mcp/run",
            json=request_data,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ Directions result: {json.dumps(result, indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct MCP call failed: {e}")
        return False

def test_crewai_tool():
    """Test CrewAI MapsMCPTool"""
    print("\n🧪 Testing CrewAI MapsMCPTool...")
    
    try:
        maps_tool = MapsMCPTool()
        
        result = maps_tool._run(
            origin="Golden Gate Bridge, San Francisco, CA",
            destination="Fisherman's Wharf, San Francisco, CA",
            mode="driving"
        )
        
        print(f"✅ CrewAI tool result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ CrewAI tool test failed: {e}")
        return False

if __name__ == "__main__":
    print("🗺️  Testing Google Maps MCP Integration")
    print("=" * 50)
    
    # Test direct MCP calls
    direct_success = test_direct_mcp_call()
    
    # Test CrewAI tool
    tool_success = test_crewai_tool()
    
    print("\n" + "=" * 50)
    if direct_success and tool_success:
        print("🎉 All Google Maps MCP tests passed!")
    else:
        print("❌ Some tests failed - check logs above")