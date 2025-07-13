"""
Planning Crew - CURRENTLY DISABLED

This crew handles route planning and itinerary creation.
Agents work together to create optimized travel routes and comprehensive itineraries.

NOTE: This crew is currently disabled because it depends on MapsMCPTool and ExaMCPTool
which have been removed from the project. To re-enable this crew, you would need to:
1. Implement alternative mapping and search tools
2. Update the agents to work with different tools or knowledge-based approaches
3. Modify the tasks to work without external API calls
"""

import weave
from crewai import Agent, Task, Crew, Process
# from tools.mcp_tools import MapsMCPTool, ExaMCPTool  # Removed - tools no longer exist


class PlanningCrew:
    """
    A crew specialized in route planning and itinerary creation.
    
    NOTE: This crew is currently disabled due to missing tool dependencies.
    
    Agents:
    - Route Planner: Creates optimized travel routes between locations
    - Itinerary Designer: Designs comprehensive daily itineraries
    """
    
    def __init__(self):
        # self.maps_tool = MapsMCPTool()  # Removed - tool no longer exists
        # self.exa_tool = ExaMCPTool()    # Removed - tool no longer exists
        print("WARNING: PlanningCrew is currently disabled due to missing tool dependencies.")
        print("MapsMCPTool and ExaMCPTool have been removed from the project.")
        self._setup_agents()
    
    def _setup_agents(self):
        """Initialize all agents for the planning crew."""
        
        self.route_planner = Agent(
            role="Route Planning Specialist",
            goal="Create optimized travel routes between locations considering time, distance, and transportation options",
            backstory="""You are an expert at route optimization and travel planning.
            You understand different transportation modes, traffic patterns, and can create
            efficient routes that maximize time and minimize travel stress. You work with
            your knowledge and reasoning to suggest optimal routes.""",
            tools=[],  # No tools available
            verbose=True,
            allow_delegation=False
        )
        
        self.itinerary_designer = Agent(
            role="Itinerary Designer",
            goal="Create comprehensive, well-timed itineraries that maximize experience value",
            backstory="""You are a master at creating engaging itineraries that balance
            activities, travel time, and personal preferences. You understand timing,
            logistics, and how to create memorable experiences using your knowledge and experience.""",
            tools=[],  # No tools available
            verbose=True,
            allow_delegation=False
        )
    
    @weave.op()
    def plan_route(self, locations: list, start_location: str, transportation_mode: str = "driving") -> dict:
        """
        Plan an optimized route through multiple locations.
        
        NOTE: This method currently returns a placeholder response due to missing tool dependencies.
        
        Args:
            locations: List of locations to visit
            start_location: Starting point for the route
            transportation_mode: Mode of transportation (driving, walking, transit, etc.)
            
        Returns:
            Dictionary containing route information and optimization details
        """
        
        print(f"WARNING: PlanningCrew.plan_route is disabled. Would have planned route from {start_location} through {locations}")
        
        # Return placeholder response
        return {
            "status": "disabled",
            "message": "PlanningCrew is currently disabled due to missing MapsMCPTool dependency",
            "requested_route": {
                "start_location": start_location,
                "locations": locations,
                "transportation_mode": transportation_mode
            },
            "suggestion": "To re-enable this functionality, implement alternative mapping tools or use knowledge-based route planning"
        }
    
    @weave.op()
    def create_itinerary(self, experiences: list, date: str, duration: str, preferences: dict = None) -> dict:
        """
        Create a comprehensive itinerary from selected experiences.
        
        NOTE: This method currently returns a placeholder response due to missing tool dependencies.
        
        Args:
            experiences: List of experiences/activities to include
            date: Target date for the itinerary
            duration: Duration of the itinerary (half-day, full-day, multi-day)
            preferences: User preferences and constraints
            
        Returns:
            Dictionary containing detailed itinerary
        """
        
        print(f"WARNING: PlanningCrew.create_itinerary is disabled. Would have created {duration} itinerary for {date}")
        
        # Return placeholder response
        return {
            "status": "disabled",
            "message": "PlanningCrew is currently disabled due to missing ExaMCPTool dependency",
            "requested_itinerary": {
                "experiences": experiences,
                "date": date,
                "duration": duration,
                "preferences": preferences
            },
            "suggestion": "To re-enable this functionality, implement alternative search tools or use knowledge-based itinerary planning"
        }
    
    @weave.op()
    def plan_complete_experience(self, experiences: list, start_location: str, 
                                date: str, duration: str, transportation_mode: str = "driving",
                                preferences: dict = None) -> dict:
        """
        Plan both route and itinerary for a complete experience.
        
        NOTE: This method currently returns a placeholder response due to missing tool dependencies.
        
        Args:
            experiences: List of experiences to include
            start_location: Starting point
            date: Target date
            duration: Duration of experience
            transportation_mode: Mode of transportation
            preferences: User preferences
            
        Returns:
            Dictionary containing complete planning results
        """
        
        print(f"WARNING: PlanningCrew.plan_complete_experience is disabled.")
        
        # Return placeholder response
        return {
            "status": "disabled",
            "message": "PlanningCrew is currently disabled due to missing tool dependencies",
            "requested_planning": {
                "experiences": experiences,
                "start_location": start_location,
                "date": date,
                "duration": duration,
                "transportation_mode": transportation_mode,
                "preferences": preferences
            },
            "suggestion": "To re-enable this functionality, implement alternative mapping and search tools"
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize Weave tracking
    weave.init("planning-crew-test")
    
    # Create planning crew
    crew = PlanningCrew()
    
    # Example: Plan a route
    locations = ["Golden Gate Bridge", "Alcatraz Island", "Fisherman's Wharf"]
    route_result = crew.plan_route(
        locations=locations,
        start_location="San Francisco, CA",
        transportation_mode="driving"
    )
    
    print("Route Planning Results:")
    print(route_result) 