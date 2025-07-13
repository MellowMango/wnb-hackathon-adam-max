"""
Podcast Content Creator Agent

Specialized agent for creating engaging podcast scripts and audio content.
"""

import os
from crewai import Agent
from crewai.llm import LLM
from tools.tts_mcp import tts_generate_audio, tts_generate_podcast

# Configure Gemini LLM
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash-exp",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# Create Podcast Content Creator Agent
podcast_creator = Agent(
    role="Podcast Content Creator",
    goal="Create engaging podcast scripts and audio content based on planned experiences",
    backstory="""You are a skilled podcaster and audio content creator.
    You excel at crafting compelling narratives, creating engaging scripts,
    and producing high-quality audio content that tells stories and shares experiences.""",
    tools=[tts_generate_audio, tts_generate_podcast],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)