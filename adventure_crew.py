"""
Adventure Transformation Crew

Main orchestrator that coordinates specialized agents to transform video transcripts
into personalized, real-world micro-adventures with full logistics and audio guides.
"""

import os
from pathlib import Path
import weave
from crewai import Task, Crew
from crewai.llm import LLM

# Import Weave tracing utilities
from weave_custom.trace_hooks import traced, setup_weave_tracing

# Import our specialized adventure agents
from agents.adventure_creative_agent import adventure_creative_agent
from agents.adventure_research_agent import adventure_research_agent
from agents.adventure_logistics_agent import adventure_logistics_agent

@traced("adventure_crew", "create_crew")
def create_adventure_crew():
    """Create and configure the adventure transformation crew."""
    
    # Create the tasks for each phase of adventure creation
    
    # Task 1: Analyze transcript and generate creative adventure ideas
    creative_task = Task(
        description="""
        Analyze the provided video transcript and generate inspiring micro-adventure ideas.
        
        You will receive a video transcript file. Your job is to:
        1. Read and understand the core themes and actionable concepts
        2. Identify elements that can be experienced in the real world
        3. Generate 2-3 specific adventure ideas that connect to the video's content
        4. Focus on universally accessible locations (parks, museums, downtown areas, etc.)
        5. Design experiences that are achievable in a few hours or a day
        
        The transcript will contain the video title, full transcript text, and metadata.
        Transform this passive content into active, engaging real-world experiences.
        """,
        expected_output="""
        A structured adventure proposal containing:
        - Adventure Title (creative and engaging)
        - Core Theme Connection (how it relates to the video)
        - 2-3 Specific Location Types to Visit
        - Key Activities to Do at each location
        - Learning Goals and discovery moments
        - Photo/Share Opportunities
        - Estimated Duration
        - Accessibility Notes
        """,
        agent=adventure_creative_agent,
        output_file="adventure_ideas.md"
    )
    
    # Task 2: Research locations and gather rich contextual information
    research_task = Task(
        description="""
        Take the adventure ideas from the Creative Agent and research specific locations
        and rich contextual information to enhance the experience.
        
        For each proposed adventure location:
        1. Use EXA to find fascinating background information, stories, and context
        2. Use Maps tools to find specific locations with addresses and directions
        3. Gather 3-5 interesting facts or stories that will make each location special
        4. Verify practical details like hours, accessibility, and requirements
        5. Generate route information and shareable links
        6. Find the best photo opportunities and unique features
        
        Focus on transforming generic location types into specific, engaging destinations
        with rich stories and practical details for a successful adventure.
        """,
        expected_output="""
        Detailed research for each location including:
        - Specific Location Details (name, address, coordinates, access info)
        - Rich Contextual Information (3-5 fascinating facts or stories)
        - Practical Information (hours, costs, accessibility, parking)
        - Experience Enhancement (best photo spots, what to look for)
        - Route Information (directions, travel time, navigation links)
        - Alternative Options (backup locations if needed)
        """,
        agent=adventure_research_agent,
        context=[creative_task],
        output_file="adventure_research.md"
    )
    
    # Task 3: Build narrative, schedule adventure, and create audio guide
    logistics_task = Task(
        description="""
        Transform the research into a complete adventure experience with compelling narrative,
        perfect scheduling, and immersive audio guide.
        
        Your responsibilities:
        1. Weave all research into a compelling, story-driven narrative
        2. Structure it as a guided tour script with clear directions and timing
        3. Create calendar events with optimal timing and complete details
        4. Generate a podcast-style audio guide script
        5. Produce the actual audio file using TTS
        6. Include all practical logistics and follow-up suggestions
        
        The final output should be a complete, ready-to-experience adventure that appears
        in the user's calendar with audio guide and all necessary details.
        """,
        expected_output="""
        Complete adventure package including:
        - Full Adventure Narrative (story-guided tour script)
        - Calendar Event (scheduled with details and links)
        - Audio Guide Script (podcast-style with timing cues)
        - Audio File (generated TTS audio guide)
        - Logistics Summary (what to bring, practical tips)
        - Follow-up Suggestions (additional exploration ideas)
        """,
        agent=adventure_logistics_agent,
        context=[creative_task, research_task],
        output_file="adventure_complete.md"
    )
    
    # Create the crew
    crew = Crew(
        agents=[adventure_creative_agent, adventure_research_agent, adventure_logistics_agent],
        tasks=[creative_task, research_task, logistics_task],
        verbose=True,
        memory=True,
        planning=True,
        planning_llm=LLM(
            model="gemini/gemini-2.0-flash-exp",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7
        )
    )
    
    return crew

@traced("adventure_crew", "transform_transcript") 
def transform_transcript_to_adventure(transcript_file: str, user_location: str = ""):
    """
    Transform a video transcript into a personalized micro-adventure.
    
    Args:
        transcript_file: Path to the transcript file
        user_location: Optional user location for personalization
        
    Returns:
        Adventure transformation results
    """
    
    # Initialize Weave tracing for this session
    setup_weave_tracing("adventure-transformation-crew")
    
    # Log the transformation start
    weave.log({
        "transcript_file": transcript_file,
        "user_location": user_location,
        "operation": "transform_transcript_to_adventure"
    })
    
    # Verify transcript file exists
    if not os.path.exists(transcript_file):
        raise FileNotFoundError(f"Transcript file not found: {transcript_file}")
    
    # Read transcript content for context
    with open(transcript_file, 'r', encoding='utf-8') as f:
        transcript_content = f.read()
    
    # Log transcript metadata
    weave.log({
        "transcript_length": len(transcript_content),
        "transcript_preview": transcript_content[:200] + "..." if len(transcript_content) > 200 else transcript_content
    })
    
    # Create the adventure crew
    crew = create_adventure_crew()
    
    # Prepare inputs for the crew
    inputs = {
        "transcript_file": transcript_file,
        "user_location": user_location or "General/Universal locations"
    }
    
    # Execute the crew with Weave tracing
    with weave.trace(name="crew_execution") as trace:
        trace.add_tag("crew_type", "adventure_transformation")
        trace.add_tag("num_agents", len(crew.agents))
        trace.add_tag("num_tasks", len(crew.tasks))
        
        try:
            # Execute the crew
            result = crew.kickoff(inputs=inputs)
            
            # Log success metrics
            weave.log({
                "status": "success",
                "result_type": type(result).__name__,
                "execution_completed": True
            })
            
            trace.add_tag("status", "completed")
            return result
            
        except Exception as e:
            # Log error
            weave.log({
                "status": "error",
                "error_type": type(e).__name__,
                "error_message": str(e)
            })
            
            trace.add_tag("status", "failed")
            trace.log_error(str(e))
            raise

if __name__ == "__main__":
    # Example usage
    transcript_file = "sample_transcript.txt"
    user_location = "Seattle, WA"  # Optional: specify user location for better recommendations
    
    try:
        result = transform_transcript_to_adventure(transcript_file, user_location)
        print(f"\n🎉 Adventure ready! Check your calendar and start exploring!")
    except Exception as e:
        print(f"❌ Error creating adventure: {e}") 