"""
Content Pipeline Flow

This module implements a structured workflow for content creation from YouTube to itinerary.
Uses CrewAI Flows for precise control over the execution pipeline.
"""

import weave
from typing import Dict, Any, List
from crewai import Flow
from crews.research_crew import ResearchCrew
from crews.planning_crew import PlanningCrew
from crews.content_crew import ContentCrew


class ContentPipeline(Flow):
    """
    A structured workflow that orchestrates the complete content creation pipeline.
    
    Pipeline stages:
    1. Research: Analyze YouTube content and find local experiences
    2. Planning: Create routes and itineraries
    3. Content: Generate podcasts and calendar events
    """
    
    def __init__(self):
        super().__init__()
        self.research_crew = ResearchCrew()
        self.planning_crew = PlanningCrew()
        self.content_crew = ContentCrew()
    
    @Flow.listen("pipeline_start")
    @weave.op()
    async def analyze_content(self, video_url: str, location: str, date: str):
        """
        Stage 1: Analyze YouTube content and discover local experiences.
        
        Args:
            video_url: YouTube video URL to analyze
            location: Target location for experiences
            date: Target date for activities
        """
        
        print(f"🎬 Starting content analysis for {video_url}")
        
        # Analyze content using research crew
        research_results = self.research_crew.analyze_content(
            video_url=video_url,
            location=location,
            date=date
        )
        
        # Store results in flow state
        self.state.research_results = research_results
        self.state.video_url = video_url
        self.state.location = location
        self.state.date = date
        
        print(f"✅ Content analysis complete - found {len(research_results.get('experiences', []))} experiences")
        
        # Trigger next stage
        await self.trigger("research_complete", research_results)
    
    @Flow.listen("research_complete")
    @weave.op()
    async def plan_experience(self, research_results: Dict[str, Any]):
        """
        Stage 2: Plan routes and create detailed itinerary.
        
        Args:
            research_results: Results from content analysis
        """
        
        print(f"🗺️  Starting experience planning")
        
        # Extract experiences from research results
        experiences = research_results.get("experiences", [])
        
        if not experiences:
            print("⚠️  No experiences found, creating basic itinerary")
            experiences = [{"name": "Default Experience", "location": self.state.location}]
        
        # Create comprehensive itinerary
        itinerary_results = self.planning_crew.plan_complete_experience(
            experiences=experiences,
            start_location=self.state.location,
            date=self.state.date,
            duration="full-day",
            transportation_mode="driving"
        )
        
        # Store planning results
        self.state.itinerary_results = itinerary_results
        self.state.experiences = experiences
        
        print(f"✅ Experience planning complete - created itinerary with {len(experiences)} stops")
        
        # Trigger content creation
        await self.trigger("planning_complete", itinerary_results)
    
    @Flow.listen("planning_complete")
    @weave.op()
    async def create_content(self, itinerary_results: Dict[str, Any]):
        """
        Stage 3: Create podcast content and calendar events.
        
        Args:
            itinerary_results: Results from planning stage
        """
        
        print(f"🎙️  Starting content creation")
        
        # Extract participants from state or use defaults
        participants = getattr(self.state, 'participants', ["example@email.com"])
        
        # Create complete content package
        content_results = self.content_crew.create_complete_content_package(
            itinerary=itinerary_results,
            participants=participants,
            podcast_theme=f"Adventure Experience in {self.state.location}",
            voice_settings={"voice": "default", "speed": 1.0}
        )
        
        # Store final results
        self.state.content_results = content_results
        
        print(f"✅ Content creation complete - podcast and calendar ready")
        
        # Trigger completion
        await self.trigger("pipeline_complete", content_results)
    
    @Flow.listen("pipeline_complete")
    @weave.op()
    async def finalize_pipeline(self, content_results: Dict[str, Any]):
        """
        Stage 4: Finalize pipeline and prepare output.
        
        Args:
            content_results: Final content creation results
        """
        
        print(f"🎉 Pipeline complete! Finalizing outputs...")
        
        # Compile final output
        final_output = {
            "pipeline_id": f"pipeline_{self.state.date}_{hash(self.state.video_url)}",
            "input": {
                "video_url": self.state.video_url,
                "location": self.state.location,
                "date": self.state.date
            },
            "research": self.state.research_results,
            "planning": self.state.itinerary_results,
            "content": self.state.content_results,
            "status": "completed",
            "artifacts": {
                "itinerary": self.state.itinerary_results,
                "podcast_script": content_results.get("podcast_script"),
                "audio_files": content_results.get("audio_files"),
                "calendar_events": content_results.get("calendar_events")
            }
        }
        
        # Store final output
        self.state.final_output = final_output
        
        print(f"✅ Pipeline finalized - all artifacts ready")
        
        return final_output
    
    @weave.op()
    async def run_complete_pipeline(self, video_url: str, location: str, date: str, 
                                   participants: List[str] = None) -> Dict[str, Any]:
        """
        Run the complete content pipeline from start to finish.
        
        Args:
            video_url: YouTube video URL to analyze
            location: Target location for experiences
            date: Target date for activities
            participants: List of participant email addresses
            
        Returns:
            Dictionary containing complete pipeline results
        """
        
        print(f"🚀 Starting complete content pipeline")
        print(f"   Video: {video_url}")
        print(f"   Location: {location}")
        print(f"   Date: {date}")
        
        # Set initial state
        self.state.participants = participants or ["example@email.com"]
        
        # Start the pipeline
        await self.trigger("pipeline_start", {
            "video_url": video_url,
            "location": location,
            "date": date
        })
        
        # Wait for completion (in real implementation, this would be event-driven)
        await self.analyze_content(video_url, location, date)
        
        return self.state.final_output
    
    @weave.op()
    async def run_research_only(self, video_url: str, location: str, date: str) -> Dict[str, Any]:
        """
        Run only the research stage of the pipeline.
        
        Args:
            video_url: YouTube video URL to analyze
            location: Target location for experiences
            date: Target date for activities
            
        Returns:
            Dictionary containing research results
        """
        
        print(f"🔍 Running research-only pipeline")
        
        research_results = self.research_crew.analyze_content(
            video_url=video_url,
            location=location,
            date=date
        )
        
        return research_results
    
    @weave.op()
    async def run_planning_only(self, experiences: List[Dict], location: str, date: str) -> Dict[str, Any]:
        """
        Run only the planning stage of the pipeline.
        
        Args:
            experiences: List of experiences to plan
            location: Target location
            date: Target date
            
        Returns:
            Dictionary containing planning results
        """
        
        print(f"📋 Running planning-only pipeline")
        
        planning_results = self.planning_crew.plan_complete_experience(
            experiences=experiences,
            start_location=location,
            date=date,
            duration="full-day"
        )
        
        return planning_results


# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    # Initialize Weave tracking
    weave.init("content-pipeline-test")
    
    async def test_pipeline():
        # Create pipeline
        pipeline = ContentPipeline()
        
        # Run complete pipeline
        result = await pipeline.run_complete_pipeline(
            video_url="https://youtube.com/watch?v=example",
            location="San Francisco, CA",
            date="2024-01-15",
            participants=["test@example.com"]
        )
        
        print("Pipeline Results:")
        print(f"Status: {result.get('status')}")
        print(f"Artifacts: {list(result.get('artifacts', {}).keys())}")
        
        return result
    
    # Run test
    asyncio.run(test_pipeline()) 