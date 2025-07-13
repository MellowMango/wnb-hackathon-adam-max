# 🎬 Adventure Transformation System

Transform passive YouTube viewing into active, real-world experiences! This system uses specialized CrewAI agents to analyze video transcripts and create personalized local micro-adventures complete with research, narratives, scheduling, and audio guides.

## 🚀 What It Does

The Adventure Transformation System takes a video transcript and transforms it into a complete real-world experience:

1. **📝 Creative Analysis**: AI analyzes the video content and generates inspiring micro-adventure ideas
2. **🔍 Location Research**: AI finds specific local locations with rich contextual information and stories
3. **📋 Experience Creation**: AI builds compelling narratives, schedules the adventure, and creates audio guides
4. **🗓️ Calendar Integration**: Adventure appears in your calendar with all details and links
5. **🎧 Audio Guide**: Podcast-style audio guide for an immersive experience

## 🎯 System Architecture

### Core Components

- **🎨 Creative Agent**: Identifies themes and suggests micro-adventures
- **🔍 Research Agent**: Uses EXA and Google Maps to find locations and context
- **📋 Logistics Agent**: Creates narratives, schedules, and audio guides
- **🤝 CrewAI Orchestration**: Manages agent collaboration and workflow

### Technology Stack

- **CrewAI**: Multi-agent orchestration framework
- **Gemini 2.0 Flash**: Large language model for intelligent processing
- **EXA**: AI-native search for rich contextual information
- **Google Maps**: Location finding and route planning
- **Google Calendar**: Adventure scheduling
- **Text-to-Speech**: Audio guide generation

## 📁 Project Structure

```
adventure-transformation-system/
├── agents/                           # Specialized CrewAI agents
│   ├── adventure_creative_agent.py   # Creative ideation specialist
│   ├── adventure_research_agent.py   # Location & context researcher
│   └── adventure_logistics_agent.py  # Narrative & scheduling coordinator
├── tools/                            # MCP tool integrations
│   ├── exa_mcp.py                   # EXA search tools
│   ├── maps_mcp.py                  # Google Maps tools
│   ├── calendar_mcp.py              # Google Calendar tools
│   └── tts_mcp.py                   # Text-to-speech tools
├── adventure_crew.py                 # Main orchestration crew
├── run_adventure_demo.py             # Demo script
├── sample_transcript.txt             # Example video transcript
└── ADVENTURE_README.md               # This file
```

## 🛠️ Setup & Installation

### 1. Environment Setup

```bash
# Install dependencies (if not already installed)
pip install crewai
pip install 'crewai[tools]'
pip install google-api-python-client
pip install exa_py
pip install requests
```

### 2. API Keys Configuration

Create a `.env` file with your API keys:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (for enhanced functionality)
EXA_API_KEY=your_exa_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
GOOGLE_CALENDAR_API_KEY=your_google_calendar_api_key_here

# MCP Server URLs (if using external servers)
EXA_MCP_URL=http://localhost:8001
MAPS_MCP_URL=http://localhost:8002
CALENDAR_MCP_URL=http://localhost:8003
TTS_MCP_URL=http://localhost:8004
```

### 3. Getting API Keys

- **Gemini API**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **EXA API**: Sign up at [exa.ai](https://exa.ai)
- **Google Maps API**: Get from [Google Cloud Console](https://console.cloud.google.com/)
- **Google Calendar API**: Same as Google Maps (enable Calendar API)

## 🎮 Usage

### Quick Start

1. **Run the system status check**:
```bash
python run_adventure_demo.py --status
```

2. **Transform a transcript into an adventure**:
```bash
python run_adventure_demo.py
```

3. **Use your own transcript**:
   - Replace `sample_transcript.txt` with your own transcript file
   - Run the demo script

### Advanced Usage

```python
from adventure_crew import transform_transcript_to_adventure

# Transform transcript to adventure
result = transform_transcript_to_adventure(
    transcript_file="your_transcript.txt",
    user_location="Your City, State"
)
```

### Custom Transcript Format

Your transcript file should include:

```
Video Title: Your Video Title Here

Transcript:

[Your full video transcript here...]

Duration: XX:XX
Channel: Channel Name
Published: Date
Views: Number
```

## 📊 Output Files

The system generates several files for your adventure:

- **📝 adventure_ideas.md**: Creative adventure concepts and themes
- **🔍 adventure_research.md**: Detailed location research with facts and context
- **🎧 adventure_complete.md**: Complete adventure guide with narrative and logistics
- **🎵 Audio files**: Generated TTS audio guides for the experience

## 🎯 Example Adventure Flow

### Input: Urban Archaeology Video Transcript
*"The Hidden History Beneath Our Feet: Urban Archaeology Secrets"*

### Output: Complete Adventure Package

1. **🎨 Creative Ideas**:
   - "Time Detective Downtown Walk"
   - Visit historic downtown, local history museum, old cemetery
   - Activities: architectural observation, artifact hunting, photo documentation

2. **🔍 Research Results**:
   - Specific locations with addresses and hours
   - Fascinating historical stories and context
   - Route planning with estimated timing
   - Photography opportunities and tips

3. **📋 Complete Experience**:
   - Compelling narrative connecting all locations
   - Calendar event scheduled at optimal time
   - 45-minute audio guide with stories and directions
   - Practical logistics and what to bring

## 🔧 System Components Detail

### Creative Agent
- **Role**: Adventure Creative Specialist
- **Goal**: Transform video content into inspiring real-world micro-adventures
- **Skills**: Theme extraction, experience design, local adaptation
- **Output**: Structured adventure proposals with activities and learning goals

### Research Agent  
- **Role**: Adventure Research Specialist
- **Goal**: Find specific locations and rich contextual information
- **Tools**: EXA search, Google Maps, location validation
- **Output**: Detailed location research with facts, stories, and practical details

### Logistics Agent
- **Role**: Adventure Logistics Coordinator  
- **Goal**: Create narratives, schedule adventures, and generate audio guides
- **Tools**: Calendar integration, text-to-speech, narrative construction
- **Output**: Complete adventure package with audio guide and scheduling

## 🎨 Customization

### Adding New Agent Types
```python
from crewai import Agent
from crewai.llm import LLM

new_agent = Agent(
    role="Your Custom Role",
    goal="Your custom goal",
    backstory="Agent background...",
    tools=[your_custom_tools],
    llm=gemini_llm
)
```

### Custom Tools Integration
```python
from crewai.tools import tool

@tool("your.custom_tool")
def your_custom_tool(param: str) -> str:
    """Your custom tool description."""
    # Your tool logic here
    return result
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure CrewAI and dependencies are installed
2. **API Key Errors**: Check your `.env` file configuration
3. **MCP Server Issues**: Verify server URLs and connectivity
4. **Transcript Format**: Ensure proper transcript file formatting

### Debug Mode

Run with verbose output to see detailed agent processing:
```python
crew = create_adventure_crew()
crew.verbose = True
result = crew.kickoff(inputs=inputs)
```

## 🚀 Advanced Features

### Seasonal Adaptations
The system can adapt adventures based on seasons and weather conditions.

### Accessibility Options
Each adventure includes accessibility notes and alternative options.

### Social Sharing
Adventures include built-in photo opportunities and shareable moments.

### Multi-City Support
The system works in any city by focusing on universally available location types.

## 🤝 Contributing

Feel free to contribute by:
- Adding new agent types
- Creating custom tools
- Improving narrative templates
- Adding new adventure categories

## 📄 License

This project is part of the A2A Hackathon and follows open-source principles.

---

## 🎉 Ready to Transform Content into Adventures?

1. Set up your API keys
2. Run the demo script
3. Watch as your video transcript becomes a real-world adventure!
4. Share your experiences and discoveries

**From Passive Viewing → Active Living** 🌟 