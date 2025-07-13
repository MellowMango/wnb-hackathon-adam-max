#!/usr/bin/env python3
"""
Adventure Transformation Demo

Demonstrates the complete workflow of transforming video transcripts into 
personalized micro-adventures with CrewAI agents and Weave tracing.
"""

import os
import sys
from pathlib import Path
import weave
from datetime import datetime

# Add the current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from adventure_crew import transform_transcript_to_adventure
from weave_custom.trace_hooks import setup_weave_tracing

@weave.op(name="adventure_demo")
def run_adventure_demo():
    """Run the complete adventure transformation demo with Weave tracing."""
    
    # Initialize Weave tracing
    print("🔧 Initializing Weave tracing...")
    try:
        setup_weave_tracing("adventure-demo")
        print("✅ Weave tracing initialized successfully!")
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize Weave tracing: {e}")
        print("   Continuing without tracing...")
    
    # Log demo start
    weave.log({
        "demo_start": datetime.now().isoformat(),
        "operation": "adventure_demo",
        "transcript_file": "sample_transcript.txt"
    })
    
    print("\n" + "="*80)
    print("🎬 ADVENTURE TRANSFORMATION DEMO")
    print("Transform passive video content into active real-world experiences!")
    print("="*80)
    
    # Check if sample transcript exists
    transcript_file = "sample_transcript.txt"
    if not os.path.exists(transcript_file):
        print(f"❌ Error: Sample transcript file '{transcript_file}' not found!")
        print("   Please make sure the sample transcript file exists in the current directory.")
        return
    
    # Read and display transcript info
    with open(transcript_file, 'r', encoding='utf-8') as f:
        transcript_content = f.read()
    
    print(f"\n📄 Processing Transcript: {transcript_file}")
    print(f"📊 Content Length: {len(transcript_content)} characters")
    print(f"📝 Preview: {transcript_content[:200]}...")
    
    # Log transcript info
    weave.log({
        "transcript_length": len(transcript_content),
        "transcript_preview": transcript_content[:200]
    })
    
    print("\n🚀 Starting Adventure Transformation Process...")
    print("👥 Activating specialized AI agents:")
    print("   🎨 Creative Agent: Analyzing content for adventure potential")
    print("   🔍 Research Agent: Finding real-world locations and context")
    print("   📱 Logistics Agent: Building complete adventure experience")
    
    try:
        # Transform the transcript with Weave tracing
        with weave.trace(name="full_transformation") as trace:
            trace.add_tag("demo_type", "adventure_transformation")
            trace.add_tag("transcript_file", transcript_file)
            
            # Execute the transformation
            result = transform_transcript_to_adventure(
                transcript_file=transcript_file,
                user_location="Urban/Downtown area"
            )
            
            # Log success
            weave.log({
                "transformation_status": "success",
                "result_type": type(result).__name__,
                "completion_time": datetime.now().isoformat()
            })
            
            trace.add_tag("status", "completed")
            
        print("\n" + "="*80)
        print("✅ ADVENTURE TRANSFORMATION COMPLETE!")
        print("="*80)
        
        # Display results
        print("\n📁 Generated Adventure Files:")
        
        # Check and display generated files
        expected_files = [
            "adventure_ideas.md",
            "adventure_research.md", 
            "adventure_complete.md"
        ]
        
        for file_path in expected_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"   ✅ {file_path} ({len(content)} characters)")
            else:
                print(f"   ❌ {file_path} (not found)")
        
        print("\n🎯 Adventure Summary:")
        print("   Your video content has been transformed into an actionable")
        print("   real-world adventure with detailed locations, activities,")
        print("   and a complete audio guide for immersive exploration!")
        
        print("\n📱 Next Steps:")
        print("   1. Review the adventure files")
        print("   2. Schedule the calendar events")
        print("   3. Download the audio guide")
        print("   4. Start your micro-adventure!")
        
        # Log final metrics
        weave.log({
            "demo_completion": "success",
            "files_generated": len([f for f in expected_files if os.path.exists(f)]),
            "total_duration": "completed"
        })
        
        return result
        
    except Exception as e:
        # Log error
        weave.log({
            "transformation_status": "error",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "completion_time": datetime.now().isoformat()
        })
        
        print(f"\n❌ Error during transformation: {e}")
        print("   Please check your configuration and try again.")
        raise

def check_system_status():
    """Check the system status and display configuration info."""
    print("\n🔍 System Status Check:")
    
    # Check environment variables
    required_env_vars = [
        "OPENAI_API_KEY",
        "GOOGLE_API_KEY",
        "EXA_API_KEY",
        "WANDB_API_KEY"
    ]
    
    env_status = {}
    for var in required_env_vars:
        value = os.getenv(var)
        env_status[var] = "✅ Set" if value else "❌ Missing"
        print(f"   {var}: {env_status[var]}")
    
    # Log environment status
    weave.log({
        "system_check": "environment_variables",
        "env_status": env_status
    })
    
    return all(os.getenv(var) for var in required_env_vars)

if __name__ == "__main__":
    try:
        # Check system status
        check_system_status()
        
        # Run the demo
        run_adventure_demo()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
        weave.log({"demo_status": "interrupted"})
    except Exception as e:
        print(f"\n💥 Demo failed: {e}")
        weave.log({
            "demo_status": "failed",
            "error": str(e)
        })
        sys.exit(1) 