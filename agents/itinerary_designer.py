"""
Itinerary Designer Agent

Specialized agent for creating comprehensive, well-timed itineraries with navigation.
"""

import os
from crewai import Agent
from crewai.llm import LLM
from tools.exa_mcp import exa_search
from tools.maps_mcp import maps_route, maps_generate_shareable_link

# Configure Gemini LLM
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash-exp",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# Create Itinerary Designer Agent
itinerary_designer = Agent(
    role="Itinerary Designer",
    goal="Create comprehensive, well-timed itineraries that maximize experience value",
    backstory="""You are a master at creating engaging itineraries that balance
    activities, travel time, and personal preferences. You understand timing,
    logistics, and how to create memorable experiences with integrated navigation.""",
    tools=[exa_search, maps_route, maps_generate_shareable_link],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)