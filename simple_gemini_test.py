#!/usr/bin/env python3
"""
Simple Gemini test without CrewAI complexity
"""

import os
import weave
from crewai.llm import LLM

@weave.op()
def test_gemini_llm():
    """Test Gemini LLM directly"""
    
    # Configure Gemini LLM using Google AI Studio API
    gemini_llm = LLM(
        model="gemini/gemini-2.0-flash-exp",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7
    )
    
    # Test simple call
    response = gemini_llm.call("Write a one-sentence description of a sunset.")
    return response

if __name__ == "__main__":
    try:
        # Initialize Weave
        weave.init("gemini-test")
        
        print("🧪 Testing Gemini LLM...")
        result = test_gemini_llm()
        print(f"✅ Gemini response: {result}")
        print("🎉 Gemini integration working!")
        
    except Exception as e:
        print(f"❌ Gemini test failed: {e}")
        import traceback
        traceback.print_exc()