#!/usr/bin/env python3
"""
CrewAI MCP Pipeline - Main Entry Point

This is the main entry point for the CrewAI + MCP + Weave application.
Provides CLI interface and REPL for interacting with the pipeline.
"""

import os
import sys
import asyncio
import argparse
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weave_custom import setup_weave_tracing
from crews import ResearchCrew, PlanningCrew, ContentCrew
from flows import ContentPipeline, EventOrchestrator


class CrewAIMCPApp:
    """
    Main application class for CrewAI MCP Pipeline.
    """
    
    def __init__(self):
        self.weave_initialized = False
        self.crews = {}
        self.flows = {}
        self._setup_components()
    
    def _setup_components(self):
        """Initialize all crews and flows."""
        
        # Initialize crews
        self.crews = {
            "research": ResearchCrew(),
            "planning": PlanningCrew(),
            "content": ContentCrew()
        }
        
        # Initialize flows
        self.flows = {
            "pipeline": ContentPipeline(),
            "orchestrator": EventOrchestrator()
        }
        
        print("✅ CrewAI MCP components initialized")
    
    def initialize_weave(self, project_name: str = "crewai-mcp-pipeline", api_key: str = None):
        """
        Initialize Weave tracing.
        
        Args:
            project_name: Name of the Weave project
            api_key: W&B API key (optional)
        """
        if not self.weave_initialized:
            try:
                setup_weave_tracing(project_name, api_key)
                self.weave_initialized = True
                print(f"✅ Weave tracing initialized for project: {project_name}")
            except Exception as e:
                print(f"⚠️  Warning: Could not initialize Weave tracing: {e}")
    
    async def run_youtube_analysis(self, video_url: str, location: str, date: str) -> Dict[str, Any]:
        """
        Run YouTube content analysis.
        
        Args:
            video_url: YouTube video URL
            location: Target location
            date: Target date
            
        Returns:
            Analysis results
        """
        print(f"🎬 Analyzing YouTube content: {video_url}")
        
        research_crew = self.crews["research"]
        result = research_crew.analyze_content(video_url, location, date)
        
        print(f"✅ Analysis complete")
        return result
    
    async def run_complete_pipeline(self, video_url: str, location: str, date: str, 
                                   participants: List[str] = None) -> Dict[str, Any]:
        """
        Run the complete content pipeline.
        
        Args:
            video_url: YouTube video URL
            location: Target location
            date: Target date
            participants: List of participant emails
            
        Returns:
            Complete pipeline results
        """
        print(f"🚀 Starting complete pipeline")
        print(f"   Video: {video_url}")
        print(f"   Location: {location}")
        print(f"   Date: {date}")
        
        pipeline = self.flows["pipeline"]
        result = await pipeline.run_complete_pipeline(video_url, location, date, participants)
        
        print(f"✅ Pipeline complete!")
        return result
    
    async def run_experience_search(self, query: str, location: str, date: str) -> Dict[str, Any]:
        """
        Search for local experiences.
        
        Args:
            query: Search query
            location: Target location
            date: Target date
            
        Returns:
            Search results
        """
        print(f"🔍 Searching for experiences: {query}")
        
        research_crew = self.crews["research"]
        result = research_crew.research_topics([query], location, date)
        
        print(f"✅ Search complete")
        return result
    
    async def run_route_planning(self, experiences: List[Dict], location: str, date: str) -> Dict[str, Any]:
        """
        Plan routes for experiences.
        
        Args:
            experiences: List of experiences
            location: Starting location
            date: Target date
            
        Returns:
            Route planning results
        """
        print(f"🗺️  Planning routes for {len(experiences)} experiences")
        
        planning_crew = self.crews["planning"]
        result = planning_crew.plan_complete_experience(experiences, location, date, "full-day")
        
        print(f"✅ Route planning complete")
        return result
    
    def print_banner(self):
        """Print application banner."""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          CrewAI MCP Pipeline                                ║
║                                                                              ║
║  🎬 YouTube Analysis  →  🔍 Experience Search  →  🗺️  Route Planning       ║
║                     →  🎙️ Podcast Creation  →  📅 Calendar Management     ║
║                                                                              ║
║  Powered by: CrewAI + MCP + W&B Weave                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
    
    def print_help(self):
        """Print help information."""
        print("""
Available Commands:
  analyze <video_url> <location> <date>          - Analyze YouTube content
  search <query> <location> <date>               - Search for local experiences
  plan <location> <date> [experiences...]        - Plan routes for experiences
  pipeline <video_url> <location> <date> [emails...] - Run complete pipeline
  status                                         - Show system status
  help                                           - Show this help message
  exit                                           - Exit the application

Examples:
  analyze https://youtube.com/watch?v=abc123 "San Francisco" "2024-01-15"
  search "photography workshops" "San Francisco" "2024-01-15"
  pipeline https://youtube.com/watch?v=abc123 "San Francisco" "2024-01-15" user@example.com
        """)
    
    def show_status(self):
        """Show system status."""
        print(f"""
System Status:
  Weave Tracing: {'✅ Enabled' if self.weave_initialized else '❌ Disabled'}
  Crews: {len(self.crews)} loaded ({', '.join(self.crews.keys())})
  Flows: {len(self.flows)} loaded ({', '.join(self.flows.keys())})
  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)
    
    async def run_repl(self):
        """Run interactive REPL."""
        self.print_banner()
        print("Welcome to the CrewAI MCP Pipeline!")
        print("Type 'help' for available commands or 'exit' to quit.")
        
        while True:
            try:
                # Get user input
                user_input = input("\n🤖 crewai-mcp> ").strip()
                
                if not user_input:
                    continue
                
                # Parse command
                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:]
                
                # Handle commands
                if command == "exit":
                    print("👋 Goodbye!")
                    break
                
                elif command == "help":
                    self.print_help()
                
                elif command == "status":
                    self.show_status()
                
                elif command == "analyze":
                    if len(args) < 3:
                        print("❌ Usage: analyze <video_url> <location> <date>")
                        continue
                    
                    result = await self.run_youtube_analysis(args[0], args[1], args[2])
                    print(f"📊 Result: {result}")
                
                elif command == "search":
                    if len(args) < 3:
                        print("❌ Usage: search <query> <location> <date>")
                        continue
                    
                    result = await self.run_experience_search(args[0], args[1], args[2])
                    print(f"📊 Result: {result}")
                
                elif command == "pipeline":
                    if len(args) < 3:
                        print("❌ Usage: pipeline <video_url> <location> <date> [emails...]")
                        continue
                    
                    participants = args[3:] if len(args) > 3 else None
                    result = await self.run_complete_pipeline(args[0], args[1], args[2], participants)
                    print(f"📊 Result: {result}")
                
                else:
                    print(f"❌ Unknown command: {command}")
                    print("Type 'help' for available commands.")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            
            except Exception as e:
                print(f"❌ Error: {e}")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="CrewAI MCP Pipeline")
    parser.add_argument("--project", default="crewai-mcp-pipeline", help="Weave project name")
    parser.add_argument("--api-key", help="W&B API key")
    parser.add_argument("--no-weave", action="store_true", help="Disable Weave tracing")
    
    # Command mode arguments
    parser.add_argument("--analyze", nargs=3, metavar=("VIDEO_URL", "LOCATION", "DATE"), 
                       help="Analyze YouTube content")
    parser.add_argument("--search", nargs=3, metavar=("QUERY", "LOCATION", "DATE"), 
                       help="Search for experiences")
    parser.add_argument("--pipeline", nargs="+", metavar="ARGS",
                       help="Run complete pipeline (VIDEO_URL LOCATION DATE [EMAILS...])")
    
    args = parser.parse_args()
    
    # Create app instance
    app = CrewAIMCPApp()
    
    # Initialize Weave if not disabled
    if not args.no_weave:
        app.initialize_weave(args.project, args.api_key)
    
    # Handle command mode
    if args.analyze:
        result = await app.run_youtube_analysis(args.analyze[0], args.analyze[1], args.analyze[2])
        print(f"Result: {result}")
        return
    
    if args.search:
        result = await app.run_experience_search(args.search[0], args.search[1], args.search[2])
        print(f"Result: {result}")
        return
    
    if args.pipeline:
        if len(args.pipeline) < 3:
            print("❌ Pipeline requires at least video_url, location, and date")
            return
        
        participants = args.pipeline[3:] if len(args.pipeline) > 3 else None
        result = await app.run_complete_pipeline(args.pipeline[0], args.pipeline[1], 
                                                args.pipeline[2], participants)
        print(f"Result: {result}")
        return
    
    # Default: run REPL
    await app.run_repl()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1) 