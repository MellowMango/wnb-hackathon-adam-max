"""
YouTube Content Analyst Agent

Specialized agent for analyzing YouTube video content and extracting actionable insights.
"""

import os
from crewai import Agent
from crewai.llm import LLM
from tools.youtube_mcp import youtube_analyze, youtube_transcribe, youtube_metadata

# Configure Gemini LLM
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash-exp",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# Create YouTube Content Analyst Agent
youtube_analyst = Agent(
    role="YouTube Content Analyst",
    goal="Extract key topics, themes, and actionable insights from YouTube videos",
    backstory="""You are an expert at analyzing video content and extracting meaningful insights.
    You can identify main topics, key themes, emotional context, and actionable information
    that can be used to plan real-world experiences.""",
    tools=[youtube_analyze, youtube_transcribe, youtube_metadata],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)