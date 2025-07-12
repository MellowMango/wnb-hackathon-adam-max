"""
Research Crew

This crew handles content analysis and local experience discovery.
Agents work together to extract insights from YouTube content and find relevant local experiences.
"""

import os
import weave

from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
from tools.mcp_tools import YouTubeMCPTool, ExaMCPTool


class ResearchCrew:
    """
    A crew specialized in content research and local experience discovery.
    
    Agents:
    - YouTube Analyst: Extracts insights from video content
    - Local Researcher: Finds relevant local experiences and events
    """
    
    def __init__(self):
        self.youtube_tool = YouTubeMCPTool()
        self.exa_tool = ExaMCPTool()
        # Configure Gemini LLM
        self.gemini_llm = LLM(
            model="gemini/gemini-2.0-flash-exp",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7
        )
        self._setup_agents()
    
    def _setup_agents(self):
        """Initialize all agents for the research crew."""
        
        self.youtube_analyst = Agent(
            role="YouTube Content Analyst",
            goal="Extract key topics, themes, and actionable insights from YouTube videos",
            backstory="""You are an expert at analyzing video content and extracting meaningful insights.
            You can identify main topics, key themes, emotional context, and actionable information
            that can be used to plan real-world experiences.""",
            tools=[self.youtube_tool],
            llm=self.gemini_llm,
            verbose=True,
            allow_delegation=False
        )
        
        self.local_researcher = Agent(
            role="Local Experience Researcher", 
            goal="Find relevant local events, activities, and experiences based on content themes",
            backstory="""You are a specialist in discovering local activities and experiences.
            You excel at connecting abstract themes and interests to concrete, available
            experiences in specific locations and timeframes.""",
            tools=[self.exa_tool],
            llm=self.gemini_llm,
            verbose=True,
            allow_delegation=False
        )
    
    @weave.op()
    def analyze_content(self, video_url: str, location: str, date: str) -> dict:
        """
        Analyze YouTube content and find related local experiences.
        
        Args:
            video_url: YouTube video URL to analyze
            location: Target location for experience discovery
            date: Target date for activities
            
        Returns:
            Dictionary containing analysis results and local experience recommendations
        """
        
        # Define tasks
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
            agent=self.youtube_analyst,
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
            agent=self.local_researcher,
            expected_output="Ranked list of local experiences with descriptions, locations, times, and relevance scores",
            context=[content_analysis_task]  # Depends on content analysis
        )
        
        # Create and execute crew
        crew = Crew(
            agents=[self.youtube_analyst, self.local_researcher],
            tasks=[content_analysis_task, local_research_task],
            process=Process.sequential,
            verbose=True,
            memory=True  # Enable memory for better collaboration
        )
        
        result = crew.kickoff()
        return result
    
    @weave.op()
    def research_topics(self, topics: list, location: str, date: str) -> dict:
        """
        Research specific topics without YouTube analysis.
        
        Args:
            topics: List of topics/themes to research
            location: Target location
            date: Target date
            
        Returns:
            Dictionary with research results
        """
        
        research_task = Task(
            description=f"""
            Research local experiences and events in {location} on {date} related to these topics:
            {', '.join(topics)}
            
            Find:
            1. Events and activities matching these topics
            2. Venues and locations of interest
            3. Timing and availability information
            4. Cost and booking requirements
            
            Provide a comprehensive list ranked by relevance.
            """,
            agent=self.local_researcher,
            expected_output="Detailed list of experiences with all practical information"
        )
        
        crew = Crew(
            agents=[self.local_researcher],
            tasks=[research_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result


# Example usage and testing
if __name__ == "__main__":
    # Initialize Weave tracking
    weave.init("research-crew-test")
    
    # Create research crew
    crew = ResearchCrew()
    
    # Example: Analyze a YouTube video
    result = crew.analyze_content(
        video_url="https://youtube.com/watch?v=example",
        location="San Francisco, CA",
        date="2024-01-15"
    )
    
    print("Research Results:")
    print(result) 