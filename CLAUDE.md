# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CrewAI-based AI agent system that creates content pipelines from YouTube videos to local experiences. The system uses Model Context Protocol (MCP) servers for external integrations and W&B Weave for observability.

## Architecture

The system follows proper CrewAI modular architecture:

1. **Individual Agent Modules** (`agents/`): Specialized, reusable agents
   - `youtube_analyst.py`: Analyzes YouTube content and extracts insights
   - `local_researcher.py`: Discovers local experiences and events
   - `route_planner.py`: Creates optimized routes with shareable Google Maps links
   - `itinerary_designer.py`: Designs comprehensive itineraries with navigation
   - `podcast_creator.py`: Creates podcast scripts and audio content
   - `calendar_manager.py`: Manages calendar events with embedded maps

2. **Central Orchestrator** (`crew.py`): Air traffic controller for all workflows
   - `ContentCreationCrew`: Main orchestrator class that coordinates all agents
   - Imports agents from individual modules for clean separation
   - Defines high-level workflows and task coordination

3. **MCP Tools** (`tools/mcp_tools.py`): CrewAI tool wrappers for external services
   - `YouTubeMCPTool`: Video analysis and transcript extraction
   - `ExaMCPTool`: Semantic search for local experiences
   - `MapsMCPTool`: Route planning and navigation
   - `CalendarMCPTool`: Calendar event management
   - `TTSMCPTool`: Text-to-speech conversion

## Configuration

The system uses YAML configuration files:

- `config/crew_config.yaml`: CrewAI agents, LLM settings, and crew configurations
- `config/mcp_config.yaml`: MCP server endpoints and connection settings
- `.env.example`: Template for required environment variables

Key LLM settings:
- Default model: `gemini-2.5-flash` 
- Fallback model: `gemini-1.5-flash`
- Temperature: 0.7
- All models configured with `thinking_budget: 0` for faster responses

## Common Development Commands

### Running the Application

```bash
# Interactive REPL mode
python main.py

# Command-line usage
python main.py --analyze <video_url> <location> <date>
python main.py --search <query> <location> <date>
python main.py --pipeline <video_url> <location> <date> [participant_emails...]

# With custom Weave project
python main.py --project my-project-name

# Disable Weave tracing
python main.py --no-weave
```

### Dependencies

```bash
# Install dependencies
pip install -r requirements.txt

# Basic Weave test
python weave_example.py

# Setup script (creates example files)
python setup.py
```

### Testing

```bash
# Run main test suite
python test.py

# Test YouTube MCP integration
python test_youtube_mcp.py

# Test central orchestrator with all agents
python crew.py

# Test main application interface
python main.py

# Test individual agent imports
python -c "from agents.youtube_analyst import youtube_analyst; print(youtube_analyst.role)"

# Test MCP tools
python -m tools.mcp_tools
```

## Environment Setup

Required environment variables (see `.env.example`):

**Core Services:**
- `WANDB_API_KEY`: W&B API key for Weave tracing
- `OPENAI_API_KEY`: OpenAI API key for CrewAI agents
- `GEMINI_API_KEY`: Google Gemini API key (primary LLM)

**MCP Servers:**
- `YOUTUBE_API_KEY`: YouTube Data API v3
- `EXA_API_KEY`: Exa Search API
- `GOOGLE_MAPS_API_KEY`: Google Maps API
- `GOOGLE_CALENDAR_CREDENTIALS_PATH`: Google Calendar OAuth2 credentials

**Optional:**
- `ANTHROPIC_API_KEY`: Anthropic Claude API
- `ELEVEN_LABS_API_KEY`: ElevenLabs TTS
- `CREWAI_API_KEY`: CrewAI+ features

## Code Patterns

### Proper CrewAI Structure

The system follows the standard CrewAI pattern with modular agents and central orchestration:

```python
# crew.py - Central orchestrator (air traffic controller)
from agents.youtube_analyst import youtube_analyst
from agents.local_researcher import local_researcher
from crewai import Crew, Task

class ContentCreationCrew:
    def __init__(self):
        self.crew = Crew(
            agents=[youtube_analyst, local_researcher, ...],
            tasks=[],  # Tasks defined dynamically
            process=Process.sequential
        )
    
    @weave.op()
    def analyze_content(self, video_url: str, location: str, date: str):
        # Define workflow tasks and execute
        return self._execute_workflow([analysis_task, research_task])
```

### Individual Agent Modules

Each agent is defined in its own module for maximum reusability:

```python
# agents/youtube_analyst.py
from crewai import Agent
from tools.mcp_tools import YouTubeMCPTool

youtube_analyst = Agent(
    role="YouTube Content Analyst",
    goal="Extract key topics and themes from videos",
    tools=[YouTubeMCPTool()],
    # ... configuration
)
```

### Modular Benefits

- **Reusable agents**: Import individual agents into custom crews
- **Clear separation**: Each agent has single responsibility
- **Easy testing**: Test agents individually or in custom combinations
- **Scalable**: Add new agents without modifying existing ones

### MCP Tool Pattern

MCP tools follow the CrewAI `BaseTool` pattern with placeholder implementations. Real MCP server calls should replace the placeholder logic in `tools/mcp_tools.py`.

### Flow Orchestration

CrewAI Flows use event-driven architecture:

```python
@Flow.listen("pipeline_start")
async def analyze_content(self, video_url: str, location: str, date: str):
    # Process stage
    await self.trigger("research_complete", results)
```

## MCP Server Architecture

The system expects MCP servers running on:
- YouTube: `http://localhost:8000`
- Exa: `http://localhost:8001` 
- Maps: `http://localhost:8002`
- Calendar: `http://localhost:8003`
- TTS: `http://localhost:8004`

Each server should implement:
- Health check endpoint: `/health`
- MCP operations: `/mcp/run`

## Observability

W&B Weave is integrated throughout:
- Initialize with `weave.init(project_name)`
- All crew operations auto-traced
- Custom tracing in `weave_custom/`
- Project default: `crewai-mcp-pipeline`

Access traces at: https://wandb.ai/[entity]/[project]/weave

## Development Notes

- All external I/O goes through MCP tools
- Crews handle business logic, never direct API calls
- Flows orchestrate multi-step workflows
- Configuration is centralized in YAML files
- All operations are observable via Weave tracing