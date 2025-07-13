"""
Local Experience Researcher Agent

Specialized agent for discovering local activities, events, and experiences.
"""

import os
from crewai import Agent
from crewai.llm import LLM
from tools.exa_mcp import exa_search, exa_find_events

# Configure Gemini LLM
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash-exp",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# Create Local Experience Researcher Agent
local_researcher = Agent(
    role="Local Experience Researcher", 
    goal="Find relevant local events, activities, and experiences based on content themes",
    backstory="""You are a specialist in discovering local activities and experiences.
    You excel at connecting abstract themes and interests to concrete, available
    experiences in specific locations and timeframes.""",
    tools=[exa_search, exa_find_events],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)