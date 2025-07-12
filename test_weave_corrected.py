#!/usr/bin/env python3
"""
Test Weave integration with corrected environment variables
"""

import os
import weave
from crewai.llm import LLM

# Use environment variables for project configuration
project_name = os.getenv("WANDB_PROJECT", "quickstart_playground")
entity_name = "guymaxphelps"  # Use actual W&B username

print(f"🧪 Testing Weave with corrected config:")
print(f"   Entity: {entity_name}")
print(f"   Project: {project_name}")

@weave.op()
def test_simple_operation(message: str) -> str:
    """Simple test operation for Weave tracing"""
    return f"Processed: {message}"

@weave.op()
def test_gemini_integration():
    """Test Gemini + Weave integration"""
    
    # Configure Gemini LLM
    gemini_llm = LLM(
        model="gemini/gemini-2.0-flash-exp",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7
    )
    
    # Make a simple call
    response = gemini_llm.call("Describe the Golden Gate Bridge in one sentence.")
    return response

@weave.op()
def test_maps_integration():
    """Test Maps MCP + Weave integration"""
    
    from tools.mcp_tools import MapsMCPTool
    
    maps_tool = MapsMCPTool()
    
    result = maps_tool._run(
        origin="Golden Gate Bridge, San Francisco",
        destination="Alcatraz Island, San Francisco",
        mode="driving"
    )
    
    return result

if __name__ == "__main__":
    try:
        # Initialize Weave with correct project/entity
        print("🚀 Initializing Weave...")
        weave.init(project_name)  # Let Weave use your default entity
        
        print("✅ Weave initialized successfully!")
        
        # Test 1: Simple operation
        print("\n🧪 Test 1: Simple operation")
        result1 = test_simple_operation("Hello from corrected Weave setup!")
        print(f"Result: {result1}")
        
        # Test 2: Gemini integration
        print("\n🧪 Test 2: Gemini + Weave")
        result2 = test_gemini_integration()
        print(f"Gemini response: {result2}")
        
        # Test 3: Maps integration
        print("\n🧪 Test 3: Maps MCP + Weave")
        result3 = test_maps_integration()
        print(f"Maps result: Success - route found")  # Don't print full JSON
        
        print("\n🎉 All Weave tests completed successfully!")
        print(f"📊 Check your traces at: https://wandb.ai/{entity_name}/{project_name}/weave")
        
    except Exception as e:
        print(f"❌ Weave test failed: {e}")
        import traceback
        traceback.print_exc()