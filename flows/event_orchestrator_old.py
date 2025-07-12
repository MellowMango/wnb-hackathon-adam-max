"""
Event Orchestrator Flow

This module implements conditional event handling and routing for different types of requests.
Uses CrewAI Flows for precise control over event-driven workflows.
"""

import weave
from typing import Dict, Any, List
from crewai import Flow
from crews.research_crew import ResearchCrew
from crews.planning_crew import PlanningCrew
from crews.content_crew import ContentCrew


class EventOrchestrator(Flow):
    """
    An event-driven orchestrator that handles different types of requests.
    
    Event Types:
    - youtube_analysis: Analyze YouTube content
    - experience_search: Search for local experiences
    - route_planning: Plan routes and itineraries
    - content_creation: Create podcasts and calendar events
    """
    
    def __init__(self):
        super().__init__()
        self.research_crew = ResearchCrew()
        self.planning_crew = PlanningCrew()
        self.content_crew = ContentCrew()
    
    @Flow.listen("youtube_analysis")
    @weave.op()
    async def handle_youtube_analysis(self, event_data: Dict[str, Any]):
        """
        Handle YouTube content analysis requests.
        
        Args:
            event_data: Event data containing video_url, location, date
        """
        
        print(f"🎬 Handling YouTube analysis event")
        
        video_url = event_data.get("video_url")
        location = event_data.get("location")
        date = event_data.get("date")
        
        # Analyze content
        result = self.research_crew.analyze_content(
            video_url=video_url,
            location=location,
            date=date
        )
        
        # Store result and trigger next event if needed
        self.state.analysis_result = result
        
        if event_data.get("auto_plan", False):
            await self.trigger("route_planning", {
                "experiences": result.get("experiences", []),
                "location": location,
                "date": date
            })
        
        return result
    
    @Flow.listen("experience_search")
    @weave.op()
    async def handle_experience_search(self, event_data: Dict[str, Any]):
        """
        Handle experience search requests.
        
        Args:
            event_data: Event data containing query, location, date
        """
        
        print(f"🔍 Handling experience search event")
        
        query = event_data.get("query")
        location = event_data.get("location")
        date = event_data.get("date")
        
        # Search for experiences
        result = self.research_crew.research_topics(
            topics=[query],
            location=location,
            date=date
        )
        
        self.state.search_result = result
        
        return result
    
    @Flow.listen("route_planning")
    @weave.op()
    async def handle_route_planning(self, event_data: Dict[str, Any]):
        """
        Handle route planning requests.
        
        Args:
            event_data: Event data containing experiences, location, date
        """
        
        print(f"🗺️  Handling route planning event")
        
        experiences = event_data.get("experiences", [])
        location = event_data.get("location")
        date = event_data.get("date")
        
        # Plan routes and itinerary
        result = self.planning_crew.plan_complete_experience(
            experiences=experiences,
            start_location=location,
            date=date,
            duration="full-day"
        )
        
        self.state.planning_result = result
        
        # Auto-trigger content creation if requested
        if event_data.get("auto_content", False):
            await self.trigger("content_creation", {
                "itinerary": result,
                "participants": event_data.get("participants", [])
            })
        
        return result
    
    @Flow.listen("content_creation")
    @weave.op()
    async def handle_content_creation(self, event_data: Dict[str, Any]):
        """
        Handle content creation requests.
        
        Args:
            event_data: Event data containing itinerary, participants
        """
        
        print(f"🎙️  Handling content creation event")
        
        itinerary = event_data.get("itinerary")
        participants = event_data.get("participants", [])
        theme = event_data.get("theme", "Adventure Experience")
        
        # Create content package
        result = self.content_crew.create_complete_content_package(
            itinerary=itinerary,
            participants=participants,
            podcast_theme=theme
        )
        
        self.state.content_result = result
        
        return result
    
    @weave.op()
    async def process_event(self, event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single event by type.
        
        Args:
            event_type: Type of event to process
            event_data: Event data dictionary
            
        Returns:
            Dictionary containing event processing results
        """
        
        print(f"🚀 Processing event: {event_type}")
        
        # Trigger the appropriate event
        await self.trigger(event_type, event_data)
        
        # Return current state
        return {
            "event_type": event_type,
            "status": "processed",
            "results": {
                "analysis": getattr(self.state, 'analysis_result', None),
                "search": getattr(self.state, 'search_result', None),
                "planning": getattr(self.state, 'planning_result', None),
                "content": getattr(self.state, 'content_result', None)
            }
        }
    
    @weave.op()
    async def process_batch_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process multiple events in sequence.
        
        Args:
            events: List of event dictionaries with 'type' and 'data' keys
            
        Returns:
            Dictionary containing batch processing results
        """
        
        print(f"📦 Processing batch of {len(events)} events")
        
        results = []
        
        for event in events:
            event_type = event.get("type")
            event_data = event.get("data", {})
            
            result = await self.process_event(event_type, event_data)
            results.append(result)
        
        return {
            "batch_size": len(events),
            "status": "completed",
            "results": results
        }


# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    # Initialize Weave tracking
    weave.init("event-orchestrator-test")
    
    async def test_orchestrator():
        # Create orchestrator
        orchestrator = EventOrchestrator()
        
        # Test single event
        result = await orchestrator.process_event("youtube_analysis", {
            "video_url": "https://youtube.com/watch?v=example",
            "location": "San Francisco, CA",
            "date": "2024-01-15",
            "auto_plan": True
        })
        
        print("Single Event Result:")
        print(f"Status: {result.get('status')}")
        
        # Test batch events
        events = [
            {
                "type": "experience_search",
                "data": {
                    "query": "photography workshops",
                    "location": "San Francisco, CA",
                    "date": "2024-01-15"
                }
            },
            {
                "type": "route_planning",
                "data": {
                    "experiences": [{"name": "Photo Workshop", "location": "Golden Gate Park"}],
                    "location": "San Francisco, CA",
                    "date": "2024-01-15"
                }
            }
        ]
        
        batch_result = await orchestrator.process_batch_events(events)
        
        print(f"\nBatch Processing Result:")
        print(f"Processed: {batch_result.get('batch_size')} events")
        print(f"Status: {batch_result.get('status')}")
        
        return result
    
    # Run test
    asyncio.run(test_orchestrator()) 