"""
Calendar & Scheduling Manager Agent

Specialized agent for creating and managing calendar invitations with embedded navigation.
"""

import os
from crewai import Agent
from crewai.llm import LLM
from tools.calendar_mcp import calendar_create_event, calendar_create_itinerary_events

# Configure Gemini LLM
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash-exp",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# Create Calendar & Scheduling Manager Agent
calendar_manager = Agent(
    role="Calendar & Scheduling Manager",
    goal="Create and manage calendar invitations and scheduling for planned experiences",
    backstory="""You are an expert at calendar management and scheduling coordination.
    You understand the importance of proper scheduling, reminders, and making sure
    all participants are properly informed about events and activities with seamless navigation.""",
    tools=[calendar_create_event, calendar_create_itinerary_events],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)