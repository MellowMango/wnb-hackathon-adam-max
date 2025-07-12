"""
Content Crew

This crew handles content creation and calendar management.
Agents work together to create engaging podcast content and manage calendar invitations.
"""

import os
import weave

from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
from tools.mcp_tools import TTSMCPTool, CalendarMCPTool


class ContentCrew:
    """
    A crew specialized in content creation and calendar management.
    
    Agents:
    - Podcast Creator: Creates engaging podcast scripts and audio content
    - Calendar Manager: Manages calendar invitations and scheduling
    """
    
    def __init__(self):
        self.tts_tool = TTSMCPTool()
        self.calendar_tool = CalendarMCPTool()
        # Configure Gemini LLM
        self.gemini_llm = LLM(
            model="gemini/gemini-2.0-flash-exp",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7
        )
        self._setup_agents()
    
    def _setup_agents(self):
        """Initialize all agents for the content crew."""
        
        self.podcast_creator = Agent(
            role="Podcast Content Creator",
            goal="Create engaging podcast scripts and audio content based on planned experiences",
            backstory="""You are a skilled podcaster and audio content creator.
            You excel at crafting compelling narratives, creating engaging scripts,
            and producing high-quality audio content that tells stories and shares experiences.""",
            tools=[self.tts_tool],
            llm=self.gemini_llm,
            verbose=True,
            allow_delegation=False
        )
        
        self.calendar_manager = Agent(
            role="Calendar & Scheduling Manager",
            goal="Create and manage calendar invitations and scheduling for planned experiences",
            backstory="""You are an expert at calendar management and scheduling coordination.
            You understand the importance of proper scheduling, reminders, and making sure
            all participants are properly informed about events and activities.""",
            tools=[self.calendar_tool],
            llm=self.gemini_llm,
            verbose=True,
            allow_delegation=False
        )
    
    @weave.op()
    def create_podcast_script(self, itinerary: dict, content_theme: str, target_audience: str = "general") -> dict:
        """
        Create a podcast script based on planned itinerary.
        
        Args:
            itinerary: Dictionary containing itinerary details
            content_theme: Theme or angle for the podcast content
            target_audience: Target audience for the podcast
            
        Returns:
            Dictionary containing podcast script and production notes
        """
        
        script_task = Task(
            description=f"""
            Create an engaging podcast script based on this itinerary:
            {itinerary}
            
            Content theme: {content_theme}
            Target audience: {target_audience}
            
            The script should:
            1. Create a compelling narrative arc
            2. Highlight the most interesting experiences
            3. Include practical tips and insights
            4. Maintain listener engagement throughout
            5. Include natural transitions between segments
            6. Provide clear calls-to-action
            
            Include timing notes and production guidance.
            """,
            agent=self.podcast_creator,
            expected_output="Comprehensive podcast script with timing notes and production guidance"
        )
        
        crew = Crew(
            agents=[self.podcast_creator],
            tasks=[script_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    @weave.op()
    def generate_audio_content(self, script: str, voice_settings: dict = None) -> dict:
        """
        Generate audio content from podcast script.
        
        Args:
            script: Podcast script text
            voice_settings: TTS voice and quality settings
            
        Returns:
            Dictionary containing audio generation results
        """
        
        audio_task = Task(
            description=f"""
            Generate high-quality audio content from this podcast script:
            {script}
            
            Voice settings: {voice_settings or 'Default settings'}
            
            Requirements:
            1. Natural speech patterns and pacing
            2. Appropriate emotional tone
            3. Clear articulation
            4. Consistent audio quality
            5. Proper breaks and pauses
            6. Professional production quality
            
            Output audio files and generation metadata.
            """,
            agent=self.podcast_creator,
            expected_output="Audio files and generation metadata"
        )
        
        crew = Crew(
            agents=[self.podcast_creator],
            tasks=[audio_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    @weave.op()
    def create_calendar_events(self, itinerary: dict, participants: list, timezone: str = "America/Los_Angeles") -> dict:
        """
        Create calendar events for planned itinerary.
        
        Args:
            itinerary: Dictionary containing itinerary details
            participants: List of participant email addresses
            timezone: Timezone for the events
            
        Returns:
            Dictionary containing calendar event creation results
        """
        
        calendar_task = Task(
            description=f"""
            Create calendar events for this itinerary:
            {itinerary}
            
            Participants: {participants}
            Timezone: {timezone}
            
            For each itinerary item, create events with:
            1. Clear, descriptive titles
            2. Detailed descriptions including Google Maps navigation links
            3. Proper start and end times with travel buffers
            4. Location information with clickable map links
            5. Travel time estimates and directions
            6. Reminder settings (15 min before each event)
            7. Participant invitations
            8. Backup contact information
            
            CRITICAL: Extract and include shareable Google Maps links from the itinerary.
            Each calendar event description should contain clickable navigation links like:
            "📍 Location: [Venue Name]
             🗺️ Directions: [Google Maps Link]
             ⏱️ Travel Time: [Duration] from previous location"
            
            Make navigation seamless for participants.
            """,
            agent=self.calendar_manager,
            expected_output="Calendar events with embedded Google Maps navigation links and logistics details"
        )
        
        crew = Crew(
            agents=[self.calendar_manager],
            tasks=[calendar_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    @weave.op()
    def send_invitations(self, events: list, message: str = None) -> dict:
        """
        Send calendar invitations to participants.
        
        Args:
            events: List of calendar events to send
            message: Optional custom message for invitations
            
        Returns:
            Dictionary containing invitation sending results
        """
        
        invitation_task = Task(
            description=f"""
            Send calendar invitations for these events:
            {events}
            
            Custom message: {message or 'Standard invitation message'}
            
            Ensure:
            1. All participants receive invitations
            2. Clear event details are included
            3. RSVP options are enabled
            4. Proper email formatting
            5. Mobile-friendly formatting
            6. Follow-up reminders are set
            
            Track delivery status and responses.
            """,
            agent=self.calendar_manager,
            expected_output="Invitation delivery status and participant responses"
        )
        
        crew = Crew(
            agents=[self.calendar_manager],
            tasks=[invitation_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    @weave.op()
    def create_complete_content_package(self, itinerary: dict, participants: list, 
                                      podcast_theme: str, voice_settings: dict = None) -> dict:
        """
        Create a complete content package including podcast and calendar events.
        
        Args:
            itinerary: Dictionary containing itinerary details
            participants: List of participant email addresses
            podcast_theme: Theme for podcast content
            voice_settings: TTS settings for audio generation
            
        Returns:
            Dictionary containing complete content package
        """
        
        # Podcast script creation
        script_task = Task(
            description=f"""
            Create a podcast script for this itinerary:
            {itinerary}
            
            Theme: {podcast_theme}
            Focus on storytelling and practical value.
            """,
            agent=self.podcast_creator,
            expected_output="Engaging podcast script with production notes"
        )
        
        # Audio generation
        audio_task = Task(
            description=f"""
            Generate high-quality audio from the podcast script.
            Voice settings: {voice_settings or 'Default'}
            Ensure professional quality output.
            """,
            agent=self.podcast_creator,
            expected_output="Professional audio files and metadata",
            context=[script_task]
        )
        
        # Calendar events creation with navigation links
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
            agent=self.calendar_manager,
            expected_output="Calendar events with embedded Google Maps navigation links ready to send"
        )
        
        crew = Crew(
            agents=[self.podcast_creator, self.calendar_manager],
            tasks=[script_task, audio_task, calendar_task],
            process=Process.sequential,
            verbose=True,
            memory=True
        )
        
        result = crew.kickoff()
        return result


# Example usage and testing
if __name__ == "__main__":
    # Initialize Weave tracking
    weave.init("content-crew-test")
    
    # Create content crew
    crew = ContentCrew()
    
    # Example itinerary
    sample_itinerary = {
        "date": "2024-01-15",
        "activities": [
            {"name": "Golden Gate Bridge Visit", "time": "9:00 AM", "location": "Golden Gate Bridge"},
            {"name": "Alcatraz Tour", "time": "11:30 AM", "location": "Alcatraz Island"},
            {"name": "Fisherman's Wharf", "time": "2:00 PM", "location": "Pier 39"}
        ]
    }
    
    # Create podcast script
    script_result = crew.create_podcast_script(
        itinerary=sample_itinerary,
        content_theme="San Francisco Adventure",
        target_audience="travel enthusiasts"
    )
    
    print("Podcast Script Results:")
    print(script_result) 