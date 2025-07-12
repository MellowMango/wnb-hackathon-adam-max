# AI Agent Architecture Blueprint

**Zero mystery meat. MCP everywhere. Observability first.**

This project follows a battle-tested architecture for building AI agent systems using Google ADK, Model-Context-Protocol (MCP), and W&B Weave for observability.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get your W&B API key:**
   - Create account at https://wandb.ai
   - Get your API key from https://wandb.ai/authorize
   - Set it as an environment variable:
     ```bash
     export WANDB_API_KEY="your-api-key-here"
     ```

3. **Run the example:**
   ```bash
   python weave_example.py
   ```

---

## 0. Guiding Principles

1. **Zero mystery meat** – every import has a home, every file has an owner.
2. **Agents do one thing** – orchestration happens in orchestrator.py, nowhere else.
3. **MCP everywhere** – external I/O is always a Model-Context-Protocol call, so you can hot-swap providers without surgery.
4. **Observability first** – every LLM transaction auto-logs to W&B Weave, every MCP call is wrapped in structured tracing.
5. **Google ADK + A2A** – follow the SDK's Agent, SequentialAgent, WorkflowAgent patterns and export an OpenAPI schema for tool discovery.

---

## 1. Repository Layout (canonical)

```
your-adk-project/
│
├── agents/                     # Pure decision-makers, no network I/O
│   ├── __init__.py
│   ├── orchestrator.py         # SequentialAgent wiring the crew together
│   ├── youtube_agent.py        # Transcript + playlist logic
│   ├── search_agent.py         # Exa / time / geo queries
│   ├── guide_agent.py          # Route + tour generation
│   ├── podcast_agent.py        # Script + TTS payload
│   └── calendar_agent.py       # Invite composer
│
├── tools/                      # Thin MCP wrappers ONLY
│   ├── __init__.py
│   ├── youtube_mcp.py          # Captions, playlist polling
│   ├── exa_mcp.py              # Semantic search
│   ├── maps_mcp.py             # Routing
│   ├── eventbrite_mcp.py       # Local events (optional)
│   ├── tts_mcp.py              # ElevenLabs / Polly
│   └── calendar_mcp.py         # Google Calendar
│
├── weave/                      # W&B Weave pipelines + dashboards
│   ├── __init__.py
│   └── trace_hooks.py          # Auto-instrumentation helpers
│
├── configs/
│   ├── agent_config.yaml       # LLM models, temp, chain-of-thought toggles
│   └── mcp_endpoints.yaml      # Base URLs & keys (read at runtime)
│
├── tests/
│   ├── test_agents.py          # PyTest: agent behaviors w/ stubs
│   └── test_tools.py           # Contract tests for each MCP wrapper
│
├── main.py                     # CLI entry: `python -m yourproject` launches REPL
├── requirements.txt            # Pin everything (see §6)
├── .env.example                # Env vars template
├── README.md                   # Quick-start & ADR links
└── .gitignore
```

---

## 2. Agents (business logic, never call the internet directly)

```python
# agents/search_agent.py
from google.adk.agents import Agent
from google.adk.tools import MCPToolset
from weave.trace_hooks import traced  # custom decorator

exa = MCPToolset("ExaMCP", endpoint="http://exa:8000/mcp")

@traced(agent="search_agent")         # pushes every chat turn to W&B Weave
class SearchAgent(Agent):
    def __init__(self):
        super().__init__(
            name="SearchAgent",
            model="gpt-4o",
            instruction="Given a transcript topic + user geo/time, "
                        "return a ranked JSON list of local experiences.",
            tools=[exa],
            output_key="venues",
        )
```

Same pattern for the other four agents. Your orchestrator.py wires them into a SequentialAgent or WorkflowAgent.

---

## 3. MCP Wrappers (FastAPI, ~30 LOC each)

```python
# tools/maps_mcp.py
from fastapi import FastAPI
import requests, os

app = FastAPI(title="MapsMCP")

GOOGLE_KEY = os.getenv("GOOGLE_MAPS_KEY")

@app.post("/mcp/run")
def run_mcp(req: dict):
    if req["method"] == "route":
        params = {
            "origin": req["args"]["origin"],
            "destination": req["args"]["destination"],
            "mode": req["args"]["mode"],
            "key": GOOGLE_KEY,
        }
        r = requests.get("https://maps.googleapis.com/maps/api/directions/json", params=params)
        r.raise_for_status()
        return r.json()
    raise ValueError("Unknown method")
```

Export OpenAPI (/openapi.json) so ADK's A2A discovery can auto-register.

---

## 4. Weave Integration (observability on by default)

```python
# weave/trace_hooks.py
import weave

def traced(agent: str):
    def decorator(cls):
        orig_call = cls.__call__
        def new_call(self, *a, **kw):
            with weave.trace(name=agent):
                return orig_call(self, *a, **kw)
        cls.__call__ = new_call
        return cls
    return decorator
```

‣ Register once in your __init__.py and every agent is traced—zero extra code.

---

## 5. Google ADK + A2A Compliance Checklist

| Requirement (2025-Q3 SDK) | Where we satisfy it |
|---------------------------|---------------------|
| Agent subclass w/ output_key | every file in agents/ |
| MCP tools with /mcp/run | each file in tools/ |
| OpenAPI for tools | FastAPI auto-exposes |
| Root orchestrator | agents/orchestrator.py |
| adk web entry-point | main.py with `if __name__ == "__main__": root.run()` |

Don't invent your own glue—stick to the SDK's primitives.

---

## 6. requirements.txt (pinned)

```
google-adk==0.5.1
fastapi==0.111.0
uvicorn[standard]==0.29.0
weave==0.46.3
openai==1.30.5
crewai==0.4.2           # optional, if you prefer CrewAI over ADK's WorkflowAgent
python-dotenv==1.0.1
pytest==8.2.0
```

---

## 7. Local dev flow

```bash
# 1. spin MCPs (dev ports) ────────────────────────────────
docker compose up exa_mcp maps_mcp calendar_mcp ...

# 2. run orchestrator REPL ───────────────────────────────
poetry shell && python -m your_adk_project.main

# 3. watch traces in Weave ───────────────────────────────
weave server  # opens localhost:3000
```

---

## 8. Hard-earned Advice

• **Don't bake secrets** – all MCP wrappers read keys from env; mount .env in Docker-Compose.
• **Contract-test tools** – each test_tools.py hits the real API in CI (tagged @external so you can skip locally).
• **Deploy MCPs first** – cloud-run them behind one gateway; your orchestrator can live on cheap Lambda later.
• **Fail loudly** – wrap every MCP error with raise_for_status() so agents get deterministic exceptions.
• **Ship the YouTube → Search → Guide → Calendar loop before touching TTS** – voice is non-critical, schedule is everything.

---

## Documentation

- [W&B Weave Quickstart](https://weave-docs.wandb.ai/quickstart)
- [W&B Weave Documentation](https://weave-docs.wandb.ai/)
- [Google ADK Documentation](https://developers.google.com/adk)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Print this out, stick it above your monitor, and build. Everything else is yak-shaving.**
