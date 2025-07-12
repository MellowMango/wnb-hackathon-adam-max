#!/usr/bin/env python3
"""
Simple test for research crew with Weave integration
"""

import os
import weave
from crews.research_crew import ResearchCrew

if __name__ == "__main__":
    try:
        # Initialize Weave with correct project name
        project_name = os.getenv("WANDB_PROJECT", "nous-hackathon-2")
        print(f"🚀 Initializing Weave with project: {project_name}")
        weave.init(project_name)
        
        print("🧪 Testing ResearchCrew with Weave tracing...")
        
        # Create research crew
        crew = ResearchCrew()
        print("✅ ResearchCrew initialized")
        
        # Test research topics (simpler than full video analysis)
        print("🔍 Testing research topics...")
        result = crew.research_topics(
            topics=["photography workshops", "outdoor activities"],
            location="San Francisco, CA", 
            date="2024-01-15"
        )
        
        print(f"✅ Research completed successfully!")
        print(f"📊 Result type: {type(result)}")
        
        # Check traces in Weave
        print(f"🎯 Check your Weave traces at: https://wandb.ai/nous-hackathon-2/{project_name}/weave")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()