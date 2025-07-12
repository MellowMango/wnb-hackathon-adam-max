"""
Planning Crew

This crew handles route planning and itinerary creation.
Agents work together to create optimized travel routes and comprehensive itineraries.
"""

import weave
from crewai import Agent, Task, Crew, Process
from tools.mcp_tools import MapsMCPTool, ExaMCPTool


class PlanningCrew:
    """
    A crew specialized in route planning and itinerary creation.
    
    Agents:
    - Route Planner: Creates optimized travel routes between locations
    - Itinerary Designer: Designs comprehensive daily itineraries
    """
    
    def __init__(self):
        self.maps_tool = MapsMCPTool()
        self.exa_tool = ExaMCPTool()
        self._setup_agents()
    
    def _setup_agents(self):
        """Initialize all agents for the planning crew."""
        
        self.route_planner = Agent(
            role="Route Planning Specialist",
            goal="Create optimized travel routes between locations considering time, distance, and transportation options",
            backstory="""You are an expert at route optimization and travel planning.
            You understand different transportation modes, traffic patterns, and can create
            efficient routes that maximize time and minimize travel stress.""",
            tools=[self.maps_tool],
            verbose=True,
            allow_delegation=False
        )
        
        self.itinerary_designer = Agent(
            role="Itinerary Designer",
            goal="Create comprehensive, well-timed itineraries that maximize experience value",
            backstory="""You are a master at creating engaging itineraries that balance
            activities, travel time, and personal preferences. You understand timing,
            logistics, and how to create memorable experiences.""",
            tools=[self.exa_tool],
            verbose=True,
            allow_delegation=False
        )
    
    @weave.op()
    def plan_route(self, locations: list, start_location: str, transportation_mode: str = "driving") -> dict:
        """
        Plan an optimized route through multiple locations.
        
        Args:
            locations: List of locations to visit
            start_location: Starting point for the route
            transportation_mode: Mode of transportation (driving, walking, transit, etc.)
            
        Returns:
            Dictionary containing route information and optimization details
        """
        
        route_task = Task(
            description=f"""
            Plan an optimized route starting from {start_location} and visiting these locations:
            {', '.join(locations)}
            
            Transportation mode: {transportation_mode}
            
            Consider:
            1. Total travel time and distance
            2. Traffic patterns and optimal timing
            3. Logical sequence of visits
            4. Parking availability (if driving)
            5. Accessibility considerations
            
            Provide a detailed route with turn-by-turn directions, estimated times, and alternatives.
            """,
            agent=self.route_planner,
            expected_output="Optimized route with directions, timing, and logistics details"
        )
        
        crew = Crew(
            agents=[self.route_planner],
            tasks=[route_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    @weave.op()
    def create_itinerary(self, experiences: list, date: str, duration: str, preferences: dict = None) -> dict:
        """
        Create a comprehensive itinerary from selected experiences.
        
        Args:
            experiences: List of experiences/activities to include
            date: Target date for the itinerary
            duration: Duration of the itinerary (half-day, full-day, multi-day)
            preferences: User preferences and constraints
            
        Returns:
            Dictionary containing detailed itinerary
        """
        
        itinerary_task = Task(
            description=f"""
            Create a {duration} itinerary for {date} including these experiences:
            {', '.join([exp.get('name', str(exp)) for exp in experiences])}
            
            User preferences: {preferences or 'None specified'}
            
            Design an itinerary that:
            1. Optimizes timing and logistics
            2. Allows sufficient time for each experience
            3. Includes buffer time for transitions
            4. Considers meal times and breaks
            5. Accounts for opening hours and availability
            6. Provides backup options
            
            Include practical details like addresses, contact info, and costs.
            """,
            agent=self.itinerary_designer,
            expected_output="Detailed itinerary with timeline, logistics, and practical information"
        )
        
        crew = Crew(
            agents=[self.itinerary_designer],
            tasks=[itinerary_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    @weave.op()
    def plan_complete_experience(self, experiences: list, start_location: str, 
                                date: str, duration: str, transportation_mode: str = "driving",
                                preferences: dict = None) -> dict:
        """
        Plan both route and itinerary for a complete experience.
        
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
        
        # Extract locations from experiences
        locations = [exp.get('location', exp.get('address', '')) for exp in experiences if exp.get('location')]
        
        # Route planning task
        route_task = Task(
            description=f"""
            Plan an optimized route from {start_location} through these experience locations:
            {', '.join(locations)}
            
            Transportation: {transportation_mode}
            Consider timing, traffic, and logistics.
            """,
            agent=self.route_planner,
            expected_output="Optimized route with travel times and directions"
        )
        
        # Itinerary creation task
        itinerary_task = Task(
            description=f"""
            Using the route information, create a {duration} itinerary for {date} that:
            1. Incorporates the planned route
            2. Schedules each experience appropriately
            3. Includes travel times between locations
            4. Accounts for user preferences: {preferences or 'None'}
            5. Provides a complete minute-by-minute schedule
            
            Make it practical and enjoyable.
            """,
            agent=self.itinerary_designer,
            expected_output="Complete itinerary with integrated route and timing",
            context=[route_task]  # Depends on route planning
        )
        
        crew = Crew(
            agents=[self.route_planner, self.itinerary_designer],
            tasks=[route_task, itinerary_task],
            process=Process.sequential,
            verbose=True,
            memory=True
        )
        
        result = crew.kickoff()
        return result


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