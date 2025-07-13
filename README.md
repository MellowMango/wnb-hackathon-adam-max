# CrewAI MCP Pipeline

A content creation pipeline that transforms content into local experiences with calendar integration and podcast content using CrewAI agents and Model Context Protocol (MCP) servers.

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Test the system
python test.py

# Run main application
python main.py
```

### Local Development
```bash
# Copy environment template (if available)
cp .env.example .env
# Edit .env with your API keys

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Architecture

This system follows proper CrewAI structure with modular agents and central orchestration:

### 🤖 Individual Agents (`agents/`)
- **YouTube Content Analyst** - Analyzes video content and extracts insights
- **Local Experience Researcher** - Finds local events and activities
- **Route Planning Specialist** - Creates optimized routes with Google Maps links
- **Itinerary Designer** - Designs comprehensive itineraries
- **Podcast Content Creator** - Creates engaging podcast scripts and audio
- **Calendar & Scheduling Manager** - Manages calendar events with navigation

### 🎛️ Central Orchestrator (`crew.py`)
- **ContentCreationCrew** - Main orchestrator that coordinates all agents
- Imports agents from individual modules for clean separation
- Defines high-level workflows and task coordination

### 🔧 MCP Tools (`tools/`)
- **youtube_mcp.py** - REMOVED - Previously contained YouTube MCP server wrappers
- **exa_mcp.py** - Thin wrappers for Exa search MCP server  
- **maps_mcp.py** - Thin wrappers for Google Maps MCP server
- **calendar_mcp.py** - Thin wrappers for Calendar MCP server
- **tts_mcp.py** - Thin wrappers for TTS MCP server

### 🖥️ MCP Servers (`mcp_servers/`)
- FastAPI servers for each external service integration
- YouTube, Exa, Google Maps, Calendar, and TTS services

## Key Features

✅ **Proper CrewAI Structure** - Modular agents with central orchestration  
✅ **Thin MCP Wrappers** - Clean separation between agents and external services  
✅ **Health Checks** - All MCP servers expose `/health` endpoints  
✅ **Local Development** - Python-based development environment  
✅ **LLM-Controlled Routing** - AI determines optimal travel routes  
✅ **Shareable Google Maps Links** - Clickable navigation in calendar events  
✅ **Calendar Integration** - Automated event creation with embedded maps  
✅ **Podcast Generation** - AI-created audio content for experiences  
✅ **W&B Weave Observability** - Complete tracing and monitoring  

## Workflows

### 1. Content Analysis
YouTube video → topics & themes → local experiences

### 2. Experience Planning  
Local experiences → optimized routes → detailed itinerary

### 3. Content Creation
Itinerary → podcast script & audio → calendar events

### 4. Complete Pipeline
YouTube video → local experiences → routes → itinerary → podcast → calendar

## Environment Setup

Required environment variables:

```bash
# Core Services
WANDB_API_KEY=your_wandb_key
OPENAI_API_KEY=your_openai_key  
GEMINI_API_KEY=your_gemini_key

# MCP Servers
YOUTUBE_API_KEY=your_youtube_key
EXA_API_KEY=your_exa_key
GOOGLE_MAPS_API_KEY=your_maps_key
GOOGLE_CALENDAR_CREDENTIALS_PATH=path/to/credentials.json

# Optional
ANTHROPIC_API_KEY=your_anthropic_key
ELEVEN_LABS_API_KEY=your_elevenlabs_key
```

## Usage Examples

```python
from crew import ContentCreationCrew

crew = ContentCreationCrew()

# Analyze YouTube content
result = crew.analyze_content(
    video_url="https://youtube.com/watch?v=abc123",
    location="San Francisco, CA", 
    date="2024-01-15"
)

# Complete pipeline
result = crew.complete_pipeline(
    video_url="https://youtube.com/watch?v=abc123",
    location="San Francisco, CA",
    date="2024-01-15", 
    participants=["user@example.com"]
)
```

## Testing

```bash
# Run all tests
python test.py

# Test specific components  
python crew.py
python main.py
```

## Development

The modular structure enables:
- **Individual agent testing** and development
- **Custom crew composition** with any subset of agents  
- **Easy scaling** by adding new specialized agents
- **Clear separation** of concerns and responsibilities

For detailed development guide, see [CLAUDE.md](CLAUDE.md).