"""
Route Planning Specialist Agent

Specialized agent for creating optimized travel routes with shareable Google Maps links.
"""

import os
from crewai import Agent
from crewai.llm import LLM
from tools.maps_mcp import maps_route, maps_generate_shareable_link, maps_itinerary_route

# Configure Gemini LLM
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash-exp",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# Create Route Planning Specialist Agent
route_planner = Agent(
    role="Route Planning Specialist",
    goal="Create optimized travel routes between locations considering time, distance, and transportation options",
    backstory="""You are an expert at route optimization and travel planning.
    You understand different transportation modes, traffic patterns, and can create
    efficient routes that maximize time and minimize travel stress. You generate shareable
    Google Maps links for seamless calendar integration.""",
    tools=[maps_route, maps_generate_shareable_link, maps_itinerary_route],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)