# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CrewAI-based AI agent system that creates content pipelines from YouTube videos to local experiences. The system uses Model Context Protocol (MCP) servers for external integrations and W&B Weave for observability.

## Architecture

The system follows a 3-tier architecture:

1. **Crews** (`crews/`): CrewAI agents that handle domain-specific tasks
   - `ResearchCrew`: Analyzes YouTube content and discovers local experiences
   - `PlanningCrew`: Creates routes and itineraries
   - `ContentCrew`: Generates podcasts and manages calendar events

2. **Flows** (`flows/`): Orchestration layer using CrewAI Flows
   - `ContentPipeline`: Complete workflow from video analysis to content creation
   - `EventOrchestrator`: Event-driven coordination between crews

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

### Testing Individual Components

```bash
# Test research crew
python -m crews.research_crew

# Test content pipeline
python -m flows.content_pipeline

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

### CrewAI Integration

All crew operations are decorated with `@weave.op()` for automatic tracing:

```python
@weave.op()
def analyze_content(self, video_url: str, location: str, date: str) -> dict:
    # Crew operations automatically traced
    result = crew.kickoff()
    return result
```

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