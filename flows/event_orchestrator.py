"""
Event Orchestrator

This module implements conditional event handling and routing for different types of requests.
Simplified version without CrewAI Flow decorators.
"""

import weave
from typing import Dict, Any, List
from crews.research_crew import ResearchCrew
from crews.planning_crew import PlanningCrew
from crews.content_crew import ContentCrew


class EventOrchestrator:
    """
    An event-driven orchestrator that handles different types of requests.
    
    Event Types:
    - youtube_analysis: Analyze YouTube content
    - experience_search: Search for local experiences
    - route_planning: Plan routes and itineraries
    - content_creation: Create podcasts and calendar events
    """
    
    def __init__(self):
        self.research_crew = ResearchCrew()
        self.planning_crew = PlanningCrew()
        self.content_crew = ContentCrew()
    
    @weave.op()
    def handle_youtube_analysis(self, event_data: Dict[str, Any]):
        """
        Handle YouTube content analysis requests.
        
        Args:
            event_data: Event data containing video_url, location, date
        """
        
        print(f"🎬 Handling YouTube analysis event")
        
        video_url = event_data.get("video_url")
        location = event_data.get("location")
        date = event_data.get("date")
        
        if not all([video_url, location, date]):
            raise ValueError("Missing required fields: video_url, location, date")
        
        # Analyze content
        result = self.research_crew.analyze_content(
            video_url=video_url,
            location=location,
            date=date
        )
        
        print(f"✅ YouTube analysis complete")
        return result
    
    @weave.op()
    def handle_experience_search(self, event_data: Dict[str, Any]):
        """
        Handle experience search requests.
        
        Args:
            event_data: Event data containing query, location, date
        """
        
        print(f"🔍 Handling experience search event")
        
        query = event_data.get("query")
        location = event_data.get("location")
        date = event_data.get("date")
        
        if not all([query, location, date]):
            raise ValueError("Missing required fields: query, location, date")
        
        # Search for experiences
        result = self.research_crew.research_topics(
            topics=[query],
            location=location,
            date=date
        )
        
        print(f"✅ Experience search complete")
        return result
    
    @weave.op()
    def handle_route_planning(self, event_data: Dict[str, Any]):
        """
        Handle route planning requests.
        
        Args:
            event_data: Event data containing experiences, start_location, date
        """
        
        print(f"🗺️  Handling route planning event")
        
        experiences = event_data.get("experiences", [])
        start_location = event_data.get("start_location")
        date = event_data.get("date")
        duration = event_data.get("duration", "full-day")
        transportation_mode = event_data.get("transportation_mode", "driving")
        
        if not all([experiences, start_location, date]):
            raise ValueError("Missing required fields: experiences, start_location, date")
        
        # Plan routes and itinerary
        result = self.planning_crew.plan_complete_experience(
            experiences=experiences,
            start_location=start_location,
            date=date,
            duration=duration,
            transportation_mode=transportation_mode
        )
        
        print(f"✅ Route planning complete")
        return result
    
    @weave.op()
    def handle_content_creation(self, event_data: Dict[str, Any]):
        """
        Handle content creation requests.
        
        Args:
            event_data: Event data containing itinerary, participants, theme
        """
        
        print(f"🎙️  Handling content creation event")
        
        itinerary = event_data.get("itinerary")
        participants = event_data.get("participants", ["example@email.com"])
        podcast_theme = event_data.get("podcast_theme", "Adventure Experience")
        voice_settings = event_data.get("voice_settings", {"voice": "default", "speed": 1.0})
        
        if not itinerary:
            raise ValueError("Missing required field: itinerary")
        
        # Create content package
        result = self.content_crew.create_complete_content_package(
            itinerary=itinerary,
            participants=participants,
            podcast_theme=podcast_theme,
            voice_settings=voice_settings
        )
        
        print(f"✅ Content creation complete")
        return result
    
    @weave.op()
    def process_event(self, event_type: str, event_data: Dict[str, Any]):
        """
        Process an event based on its type.
        
        Args:
            event_type: Type of event to process
            event_data: Event data dictionary
            
        Returns:
            Event processing result
        """
        
        print(f"🎯 Processing {event_type} event")
        
        if event_type == "youtube_analysis":
            return self.handle_youtube_analysis(event_data)
        elif event_type == "experience_search":
            return self.handle_experience_search(event_data)
        elif event_type == "route_planning":
            return self.handle_route_planning(event_data)
        elif event_type == "content_creation":
            return self.handle_content_creation(event_data)
        else:
            raise ValueError(f"Unknown event type: {event_type}")
    
    @weave.op()
    def process_batch_events(self, events: List[Dict[str, Any]]):
        """
        Process a batch of events in sequence.
        
        Args:
            events: List of events to process
            
        Returns:
            List of event processing results
        """
        
        print(f"📦 Processing batch of {len(events)} events")
        
        results = []
        for i, event in enumerate(events):
            print(f"🔄 Processing event {i+1}/{len(events)}")
            
            event_type = event.get("event_type")
            event_data = event.get("event_data", {})
            
            try:
                result = self.process_event(event_type, event_data)
                results.append({
                    "event_index": i,
                    "event_type": event_type,
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                print(f"❌ Event {i+1} failed: {e}")
                results.append({
                    "event_index": i,
                    "event_type": event_type,
                    "status": "error",
                    "error": str(e)
                })
        
        print(f"✅ Batch processing complete")
        return results


# Example usage and testing
if __name__ == "__main__":
    # Initialize Weave tracking
    weave.init("event-orchestrator-test")
    
    # Create orchestrator
    orchestrator = EventOrchestrator()
    
    # Test single event
    test_event_data = {
        "video_url": "https://youtube.com/watch?v=example",
        "location": "San Francisco, CA",
        "date": "2024-01-15"
    }
    
    result = orchestrator.process_event("youtube_analysis", test_event_data)
    print("Event Processing Results:")
    print(f"Status: Completed")