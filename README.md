# 🎬 DueTube

Transform passive YouTube content into active real-world micro-adventures! This system uses specialized CrewAI agents to analyze video transcripts and create personalized, location-based experiences with complete logistics, audio guides, and calendar integration.

## 🚀 What This System Does

**Input**: Video transcript (educational content, tutorials, documentaries)  
**Output**: Complete real-world adventure with:
- 🎯 Creative adventure concepts connecting to video themes
- 📍 Researched locations with rich contextual information
- 🎧 Audio guides for immersive exploration
- 📅 Calendar events with navigation and scheduling
- 🗺️ Interactive maps and route planning

## 🏗️ Architecture

### 🤖 Specialized AI Agents

**Creative Agent** (`agents/adventure_creative_agent.py`)
- Analyzes video transcripts for adventure potential
- Generates creative micro-adventure concepts
- Identifies universally accessible locations
- Designs achievable experiences (2-6 hours)

**Research Agent** (`agents/adventure_research_agent.py`)
- Uses EXA contextual search for location discovery
- Integrates Google Maps for detailed location data
- Finds opening hours, costs, and accessibility info
- Provides rich historical and cultural context

**Logistics Agent** (`agents/adventure_logistics_agent.py`)
- Creates compelling narrative structures
- Generates text-to-speech audio guides
- Schedules calendar events with navigation
- Builds complete adventure packages

### 🎛️ Orchestration System

**Adventure Crew** (`adventure_crew.py`)
- Main orchestrator coordinating all agents
- Handles task dependencies and workflow
- Manages inputs/outputs between agents
- Includes comprehensive Weave tracing

### 🔧 MCP Integration

**Tool Wrappers** (`tools/`)
- `exa_mcp.py` - Contextual search integration
- `maps_mcp.py` - Google Maps API wrapper
- `calendar_mcp.py` - Calendar event management
- `tts_mcp.py` - Text-to-speech generation

**MCP Servers** (`mcp_servers/`)
- FastAPI servers for external service integration
- Health checks and error handling
- Standardized API interfaces

### 📊 Evaluation & Observability

**Weave Integration** (`weave_custom/`)
- Complete tracing of agent interactions
- Performance monitoring and metrics
- Error tracking and debugging
- Real-time dashboard insights

**Evaluation System** (`evaluate_adventure_system.py`)
- **Creativity Metrics**: Theme connection, creative elements
- **Feasibility Assessment**: Location details, practical info
- **Engagement Analysis**: Interactive elements, photo opportunities
- Automated scoring and reporting

## 🛠️ Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/wnb-hackathon-adam-max.git
cd wnb-hackathon-adam-max

# Run automated setup
python setup_weave_eval.py
```

### 2. Configure API Keys

Create a `.env` file with your API keys:

```bash
# Copy the template
cp .env.template .env

# Edit with your keys
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here
EXA_API_KEY=your_exa_key_here
WANDB_API_KEY=your_wandb_key_here

# Optional: Advanced configuration
WANDB_PROJECT=adventure-system-evaluation
WEAVE_TRACE_AGENTS=true
WEAVE_TRACE_TASKS=true
```

### 3. Test the System

```bash
# Run the demo
python run_adventure_demo.py

# Run comprehensive evaluations
python evaluate_adventure_system.py
```

## 📖 Usage Examples

### Basic Adventure Creation

```python
from adventure_crew import transform_transcript_to_adventure

# Transform a transcript into an adventure
result = transform_transcript_to_adventure(
    transcript_file="sample_transcript.txt",
    user_location="Downtown Seattle"
)

# Check generated files
# - adventure_ideas.md: Creative concepts
# - adventure_research.md: Location details
# - adventure_complete.md: Full adventure package
```

### Advanced Evaluation

```python
from evaluate_adventure_system import AdventureEvaluator

# Create evaluator
evaluator = AdventureEvaluator("my-evaluation-project")

# Add custom test case
evaluator.add_test_case(
    name="Nature Photography",
    transcript_content="Video about golden hour photography...",
    expected_themes=["photography", "nature", "lighting"]
)

# Run evaluation
results = evaluator.run_full_evaluation()
```

## 🎯 Key Features

### ✅ Complete Adventure Pipeline
- **Video → Adventure**: Transform any educational content
- **Smart Location Finding**: Uses EXA + Google Maps for discovery
- **Narrative Building**: Creates compelling story-driven experiences
- **Audio Guides**: TTS-generated immersive audio

### ✅ Advanced AI Orchestration
- **CrewAI Framework**: Specialized agents with clear roles
- **Task Dependencies**: Coordinated workflow execution
- **Error Handling**: Robust failure recovery
- **Flexible Input**: Works with any transcript format

### ✅ Comprehensive Evaluation
- **Multi-Metric Scoring**: Creativity, feasibility, engagement
- **Automated Testing**: Multiple test cases and scenarios
- **Weave Integration**: Full observability and tracing
- **Performance Analytics**: Real-time monitoring

### ✅ Production Ready
- **Docker Support**: Containerized deployment
- **Health Checks**: Service monitoring
- **Scalable Architecture**: Modular design
- **API Documentation**: Complete MCP integration

## 🔍 Evaluation Metrics

The system includes comprehensive evaluation capabilities:

### Creativity Score (0-1)
- Theme connection to original video
- Creative element richness
- Adventure concept originality

### Feasibility Score (0-1)
- Location accessibility information
- Practical implementation details
- Cost and timing considerations

### Engagement Score (0-1)
- Interactive elements and activities
- Photo and sharing opportunities
- Memorable experience design

## 🏃‍♂️ Running the System

### Demo Mode
```bash
python run_adventure_demo.py
```
- Uses sample transcript
- Full end-to-end demonstration
- Weave tracing enabled
- Output files generated

### Evaluation Mode
```bash
python evaluate_adventure_system.py
```
- Runs multiple test cases
- Generates detailed metrics
- Saves results to JSON
- Weave dashboard integration

### Custom Transcript
```python
from adventure_crew import transform_transcript_to_adventure

result = transform_transcript_to_adventure(
    transcript_file="your_transcript.txt",
    user_location="Your City"
)
```

## 📁 Project Structure

```
├── agents/                          # Specialized AI agents
│   ├── adventure_creative_agent.py  # Creative ideation
│   ├── adventure_research_agent.py  # Location research
│   └── adventure_logistics_agent.py # Logistics & audio
├── tools/                           # MCP tool wrappers
│   ├── exa_mcp.py                  # EXA search integration
│   ├── maps_mcp.py                 # Google Maps wrapper
│   ├── calendar_mcp.py             # Calendar management
│   └── tts_mcp.py                  # Text-to-speech
├── mcp_servers/                     # MCP server implementations
│   ├── exa_server.py               # EXA search server
│   ├── maps_server.py              # Google Maps server
│   ├── calendar_server.py          # Calendar server
│   └── youtube_server.py           # YouTube server
├── weave_custom/                    # Weave integration
│   ├── config.py                   # Weave configuration
│   ├── instrumentation.py          # Observability tools
│   └── trace_hooks.py              # Tracing decorators
├── adventure_crew.py                # Main orchestration
├── run_adventure_demo.py            # Demo script
├── evaluate_adventure_system.py     # Evaluation system
├── setup_weave_eval.py             # Setup automation
└── sample_transcript.txt           # Example input
```

## 🌐 API Integration

### EXA Search
- Contextual search for location discovery
- Rich content and context retrieval
- Neural search capabilities

### Google Maps
- Location details and coordinates
- Opening hours and contact info
- Route planning and navigation

### Calendar Services
- Event creation and scheduling
- Navigation link embedding
- Participant management

### Text-to-Speech
- Audio guide generation
- Multiple voice options
- High-quality output

## 📊 Monitoring & Observability

### Weave Dashboard
- Real-time execution tracing
- Performance metrics
- Error tracking and debugging
- Agent interaction visualization

### Evaluation Reports
- Detailed scoring breakdowns
- Comparative analysis
- Trend tracking over time
- Custom metric definitions

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Production deployment
docker-compose -f docker-compose.prod.yml up
```

## 🧪 Testing

### Unit Tests
```bash
pytest tests/
```

### Integration Tests
```bash
python -m pytest tests/integration/
```

### Evaluation Tests
```bash
python evaluate_adventure_system.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the evaluation suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI** - Multi-agent orchestration framework
- **Weights & Biases Weave** - Observability and evaluation
- **EXA** - Contextual search capabilities
- **Google Maps API** - Location and navigation services

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the [documentation](docs/)
- Review the [troubleshooting guide](docs/troubleshooting.md)

---

**Transform your passive viewing into active adventures!** 🎬 → 🗺️ → 🎧 → 📅
