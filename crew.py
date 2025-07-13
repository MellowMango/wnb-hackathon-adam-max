"""
Central Crew Orchestrator

This is the air traffic controller for the entire CrewAI pipeline.
It coordinates all agents and defines high-level workflows.
"""

import weave
from crewai import Crew, Task, Process

# Import all specialized agents
from agents.youtube_analyst import youtube_analyst
from agents.local_researcher import local_researcher
from agents.route_planner import route_planner
from agents.itinerary_designer import itinerary_designer
from agents.podcast_creator import podcast_creator
from agents.calendar_manager import calendar_manager


class ContentCreationCrew:
    """
    Central orchestrator for the content creation pipeline.
    
    This crew coordinates all agents to transform YouTube content into
    local experiences with calendar integration and podcast content.
    """
    
    def __init__(self):
        """Initialize the crew with all specialized agents."""
        self.crew = Crew(
            agents=[
                youtube_analyst,
                local_researcher,
                route_planner,
                itinerary_designer,
                podcast_creator,
                calendar_manager
            ],
            tasks=[],  # Tasks are defined dynamically for each workflow
            process=Process.sequential,
            verbose=True
        )
    
    def _execute_workflow(self, tasks: list):
        """Execute a workflow with the given tasks."""
        # Create a temporary crew with specific tasks
        workflow_crew = Crew(
            agents=[
                youtube_analyst,
                local_researcher,
                route_planner,
                itinerary_designer,
                podcast_creator,
                calendar_manager
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        return workflow_crew.kickoff()
    
    @weave.op()
    def analyze_content(self, video_url: str, location: str, date: str):
        """
        Workflow: Analyze YouTube content and find local experiences.
        
        Agents involved: YouTube Analyst → Local Researcher
        """
        
        content_analysis_task = Task(
            description=f"""
            Analyze the YouTube video at {video_url} and extract:
            1. Main topics and themes discussed
            2. Key insights and takeaways
            3. Emotional context and mood
            4. Actionable interests that could translate to real-world activities
            5. Target audience and demographics
            
            Return a structured JSON with these insights.
            """,
            agent=youtube_analyst,
            expected_output="JSON object with topics, themes, insights, mood, and actionable_interests"
        )
        
        local_research_task = Task(
            description=f"""
            Based on the YouTube content analysis, find relevant local experiences in {location} on {date}.
            
            Focus on:
            1. Activities that match the content themes
            2. Events happening on the specified date
            3. Experiences that align with the emotional context
            4. Opportunities for hands-on engagement
            
            Rank results by relevance and provide practical details.
            """,
            agent=local_researcher,
            expected_output="Ranked list of local experiences with descriptions, locations, times, and relevance scores",
            context=[content_analysis_task]
        )
        
        return self._execute_workflow([content_analysis_task, local_research_task])
    
    @weave.op()
    def plan_experience(self, experiences: list, start_location: str, date: str, 
                       duration: str = "full-day", transportation_mode: str = "driving"):
        """
        Workflow: Plan routes and create itinerary with shareable links.
        
        Agents involved: Route Planner → Itinerary Designer
        """
        
        # Extract locations from experiences
        locations = [exp.get('location', exp.get('address', '')) for exp in experiences if exp.get('location')]
        
        route_task = Task(
            description=f"""
            Plan an optimized route from {start_location} through these experience locations:
            {', '.join(locations)}
            
            Transportation: {transportation_mode}
            
            IMPORTANT: Use the generate_itinerary_route method to create:
            1. Optimized route order for efficiency
            2. Individual shareable Google Maps links for each leg
            3. Complete route link for the entire journey
            4. Calendar-ready descriptions with links
            5. Accurate travel times and distances
            
            The output must include shareable links that can be embedded in calendar invitations.
            """,
            agent=route_planner,
            expected_output="Complete route with shareable Google Maps links for calendar integration"
        )
        
        itinerary_task = Task(
            description=f"""
            Using the route information with shareable links, create a {duration} itinerary for {date} that:
            1. Incorporates the planned route with Google Maps links
            2. Schedules each experience appropriately with travel buffers
            3. Includes individual shareable links for each travel segment
            4. Provides calendar-ready event descriptions with navigation links
            5. Creates a complete minute-by-minute schedule
            6. Formats information for easy calendar integration
            
            IMPORTANT: Preserve all shareable Google Maps links from the route planning for calendar integration.
            Each experience should have associated navigation links that can be clicked from calendar invites.
            """,
            agent=itinerary_designer,
            expected_output="Complete itinerary with shareable Google Maps links ready for calendar integration",
            context=[route_task]
        )
        
        return self._execute_workflow([route_task, itinerary_task])
    
    @weave.op()
    def create_content(self, itinerary: dict, participants: list, podcast_theme: str = None):
        """
        Workflow: Create podcast content and calendar events.
        
        Agents involved: Podcast Creator → Calendar Manager
        """
        
        script_task = Task(
            description=f"""
            Create a podcast script for this itinerary:
            {itinerary}
            
            Theme: {podcast_theme or 'Local Experience Adventure'}
            Focus on storytelling and practical value.
            """,
            agent=podcast_creator,
            expected_output="Engaging podcast script with production notes"
        )
        
        audio_task = Task(
            description=f"""
            Generate high-quality audio from the podcast script.
            Ensure professional quality output.
            """,
            agent=podcast_creator,
            expected_output="Professional audio files and metadata",
            context=[script_task]
        )
        
        calendar_task = Task(
            description=f"""
            Create calendar events for the itinerary participants: {participants}
            
            CRITICAL REQUIREMENTS:
            1. Extract shareable Google Maps links from the itinerary data
            2. Include clickable navigation links in each calendar event description
            3. Add travel time estimates between locations
            4. Format descriptions for mobile and desktop viewing
            5. Coordinate timing with the podcast content timeline
            6. Set appropriate reminders and notifications
            
            Each event must have clear navigation instructions with working Google Maps links.
            """,
            agent=calendar_manager,
            expected_output="Calendar events with embedded Google Maps navigation links ready to send"
        )
        
        return self._execute_workflow([script_task, audio_task, calendar_task])
    
    @weave.op()
    def complete_pipeline(self, video_url: str, location: str, date: str, 
                         participants: list, duration: str = "full-day",
                         transportation_mode: str = "driving", podcast_theme: str = None):
        """
        Complete end-to-end pipeline workflow.
        
        Agents involved: All agents in sequence
        YouTube Analyst → Local Researcher → Route Planner → Itinerary Designer → Podcast Creator → Calendar Manager
        """
        
        analysis_task = Task(
            description=f"""
            Analyze the YouTube video at {video_url} and extract key topics and themes.
            Return actionable insights for real-world experience planning.
            """,
            agent=youtube_analyst,
            expected_output="Video analysis with topics and themes"
        )
        
        research_task = Task(
            description=f"""
            Based on the video analysis, find relevant local experiences in {location} on {date}.
            Focus on activities that match the content themes and are practically available.
            """,
            agent=local_researcher,
            expected_output="List of relevant local experiences with details",
            context=[analysis_task]
        )
        
        route_task = Task(
            description=f"""
            Plan an optimized route for the discovered experiences using {transportation_mode}.
            Generate shareable Google Maps links for each route segment for calendar integration.
            """,
            agent=route_planner,
            expected_output="Optimized route with shareable Google Maps links",
            context=[research_task]
        )
        
        itinerary_task = Task(
            description=f"""
            Create a complete {duration} itinerary incorporating the route with shareable links.
            Include timing, logistics, and calendar-ready descriptions.
            """,
            agent=itinerary_designer,
            expected_output="Complete itinerary with navigation links",
            context=[route_task]
        )
        
        script_task = Task(
            description=f"""
            Create an engaging podcast script based on the planned itinerary.
            Theme: {podcast_theme or 'Local Experience Adventure'}
            """,
            agent=podcast_creator,
            expected_output="Podcast script with production notes",
            context=[itinerary_task]
        )
        
        calendar_task = Task(
            description=f"""
            Create calendar events for participants: {participants}
            Include shareable Google Maps links from the itinerary in each event description.
            Ensure seamless navigation for all participants.
            """,
            agent=calendar_manager,
            expected_output="Calendar events with embedded navigation links",
            context=[itinerary_task]
        )
        
        return self._execute_workflow([
            analysis_task, research_task, route_task, 
            itinerary_task, script_task, calendar_task
        ])
    
    # Individual agent testing methods
    @weave.op()
    def test_youtube_analyst(self, video_url: str):
        """Test YouTube analyst individually."""
        task = Task(
            description=f"Analyze YouTube video: {video_url}. Extract topics, themes, and insights.",
            agent=youtube_analyst,
            expected_output="Analysis results with topics and themes"
        )
        return self._execute_workflow([task])
    
    @weave.op()
    def test_local_researcher(self, topics: list, location: str, date: str):
        """Test local researcher individually."""
        task = Task(
            description=f"Find local experiences in {location} on {date} for topics: {topics}",
            agent=local_researcher,
            expected_output="List of relevant local experiences"
        )
        return self._execute_workflow([task])
    
    @weave.op()
    def test_route_planner(self, experiences: list, start_location: str):
        """Test route planner individually."""
        locations = [exp.get('location', '') for exp in experiences]
        task = Task(
            description=f"Plan optimized route from {start_location} through {locations} with shareable links",
            agent=route_planner,
            expected_output="Route with Google Maps links"
        )
        return self._execute_workflow([task])
    
    @weave.op()
    def test_itinerary_designer(self, experiences: list, date: str):
        """Test itinerary designer individually."""
        task = Task(
            description=f"Create itinerary for {date} with experiences: {experiences}",
            agent=itinerary_designer,
            expected_output="Detailed itinerary with timing"
        )
        return self._execute_workflow([task])
    
    @weave.op()
    def test_podcast_creator(self, itinerary: dict, theme: str):
        """Test podcast creator individually."""
        task = Task(
            description=f"Create podcast script for itinerary: {itinerary} with theme: {theme}",
            agent=podcast_creator,
            expected_output="Podcast script with production notes"
        )
        return self._execute_workflow([task])
    
    @weave.op()
    def test_calendar_manager(self, itinerary: dict, participants: list):
        """Test calendar manager individually."""
        task = Task(
            description=f"Create calendar events for itinerary: {itinerary} with participants: {participants}",
            agent=calendar_manager,
            expected_output="Calendar events with navigation links"
        )
        return self._execute_workflow([task])


# Create the main crew instance for import
crew = ContentCreationCrew()


# Example usage and testing
if __name__ == "__main__":
    # Initialize Weave tracking
    weave.init("content-creation-crew")
    
    print("🎯 CrewAI Content Creation Orchestrator")
    print("📋 Testing individual agents...")
    
    # Test individual agents
    print("\n1. Testing YouTube Analyst:")
    youtube_result = crew.test_youtube_analyst("https://youtube.com/watch?v=example")
    print(f"   Result: {type(youtube_result)}")
    
    # Test complete pipeline
    print("\n2. Testing Complete Pipeline:")
    pipeline_result = crew.complete_pipeline(
        video_url="https://youtube.com/watch?v=example",
        location="San Francisco, CA",
        date="2024-01-15",
        participants=["test@example.com"],
        podcast_theme="San Francisco Adventure"
    )
    print(f"   Result: {type(pipeline_result)}")
    
    print("\n✅ Crew orchestration complete!")