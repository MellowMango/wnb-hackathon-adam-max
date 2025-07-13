"""
YouTube MCP Tool Wrapper

Thin wrapper for YouTube MCP server calls.
"""

import os
import requests
from crewai.tools import tool
from typing import Dict, Any

BASE_URL = os.getenv("YOUTUBE_MCP_URL", "http://localhost:8000")

@tool("youtube.transcribe")
def youtube_transcribe(video_url: str, lang: str = "en") -> str:
    """Extract transcript/captions from YouTube video."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "get_transcript",
                "args": {
                    "video_url": video_url,
                    "lang": lang
                }
            },
            timeout=45
        )
        response.raise_for_status()
        result = response.json()
        return result.get("transcript", "")
    except Exception as e:
        return f"Error transcribing video: {str(e)}"

@tool("youtube.analyze")
def youtube_analyze(video_url: str, analysis_type: str = "full") -> Dict[str, Any]:
    """Analyze YouTube video content and extract insights."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "analyze_video",
                "args": {
                    "video_url": video_url,
                    "analysis_type": analysis_type
                }
            },
            timeout=45
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # Fallback data for testing
        return {
            "video_url": video_url,
            "analysis_type": analysis_type,
            "title": "Sample Video Title",
            "description": "Sample video description...",
            "duration": "10:30",
            "captions": "Sample transcript content...",
            "themes": ["adventure", "travel", "exploration"],
            "actionable_insights": [
                "Interest in outdoor activities",
                "Preference for guided experiences",
                "Focus on photography opportunities"
            ],
            "target_audience": "adventure seekers",
            "mood": "excited and adventurous",
            "error": str(e),
            "fallback": True
        }

@tool("youtube.metadata")
def youtube_metadata(video_url: str) -> Dict[str, Any]:
    """Get YouTube video metadata."""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/run",
            json={
                "method": "get_metadata",
                "args": {"video_url": video_url}
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "video_url": video_url,
            "title": "Sample Video",
            "description": "Sample description",
            "duration": "10:00",
            "error": str(e),
            "fallback": True
        }