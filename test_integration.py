#!/usr/bin/env python3
"""
Test script for Gemini + CrewAI + W&B integration
"""

import os
import weave
from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM

def test_gemini_integration():
    """Test basic Gemini integration with CrewAI"""
    
    print("🧪 Testing Gemini + CrewAI integration...")
    
    # Initialize Weave
    weave.init("integration-test")
    
    # Configure Gemini LLM
    gemini_llm = LLM(
        model="gemini-2.0-flash-exp",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7
    )
    
    # Create a simple test agent
    test_agent = Agent(
        role="Test Agent",
        goal="Generate a simple creative response",
        backstory="You are a helpful test agent that responds creatively to prompts.",
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False
    )
    
    # Create a simple task
    test_task = Task(
        description="Write a short, creative description of a sunset over mountains.",
        agent=test_agent,
        expected_output="A 2-3 sentence creative description of a sunset"
    )
    
    # Create and run crew
    crew = Crew(
        agents=[test_agent],
        tasks=[test_task],
        process=Process.sequential,
        verbose=True
    )
    
    print("🚀 Running crew with Gemini...")
    result = crew.kickoff()
    
    print("✅ Integration test completed!")
    print(f"Result: {result}")
    
    return result

if __name__ == "__main__":
    try:
        result = test_gemini_integration()
        print("\n🎉 Success! Gemini + CrewAI + W&B integration is working!")
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()