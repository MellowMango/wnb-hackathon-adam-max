"""
TTS MCP Tool Wrapper

Thin wrapper for Text-to-Speech MCP server calls.
"""

import os
import requests
from crewai.tools import tool
from typing import Dict, Any

BASE_URL = os.getenv("TTS_MCP_URL", "http://localhost:8004")

@tool("tts.generate_audio")
def tts_generate_audio(
    text: str,
    voice: str = "default",
    speed: float = 1.0
) -> Dict[str, Any]:
    """Generate audio from text using TTS."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "generate_audio",
                "args": {
                    "text": text,
                    "voice": voice,
                    "speed": speed
                }
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "audio_url": "fallback://no-audio-generated",
            "text": text,
            "voice": voice,
            "speed": speed,
            "duration": len(text) / 10,  # Rough estimate
            "status": "fallback",
            "error": str(e),
            "fallback": True
        }

@tool("tts.generate_podcast")
def tts_generate_podcast(
    script: str,
    title: str = "Generated Podcast",
    voice_settings: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Generate a complete podcast from script."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "generate_podcast",
                "args": {
                    "script": script,
                    "title": title,
                    "voice_settings": voice_settings or {}
                }
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "podcast_url": "fallback://no-podcast-generated",
            "title": title,
            "script": script,
            "duration": len(script) / 8,  # Rough estimate
            "voice_settings": voice_settings or {},
            "status": "fallback",
            "error": str(e),
            "fallback": True
        }

@tool("tts.health_check")
def tts_health_check() -> Dict[str, Any]:
    """Check if TTS service is healthy."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        response.raise_for_status()
        return {"status": "healthy", "service": "tts"}
    except Exception as e:
        return {"status": "unhealthy", "service": "tts", "error": str(e)}