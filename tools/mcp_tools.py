"""
MCP Tools Package - Simplified for ytmcp only

This module contains CrewAI tool wrappers for the YouTube transcript MCP server.
"""

import os
import json
import subprocess
import sys
from typing import Dict, Any, List, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class YouTubeMCPTool(BaseTool):
    """
    Tool for interacting with YouTube content via ytmcp MCP server.
    Provides transcript extraction and video analysis capabilities.
    """
    
    name: str = "youtube_mcp"
    description: str = """
    Extract YouTube video transcripts and analyze content using the ytmcp MCP server.
    
    Capabilities:
    - Extract video transcripts/captions
    - Get video metadata (title, description, duration)
    - Analyze transcript content for themes and insights
    - Support for multiple languages
    """
    
    def __init__(self):
        super().__init__()
    
    def _run(self, action: str, **kwargs) -> str:
        """
        Run YouTube operations via ytmcp MCP server.
        
        Args:
            action: Action to perform (get_transcript, analyze_video, get_metadata)
            **kwargs: Additional parameters specific to each action
            
        Returns:
            JSON string with operation results
        """
        
        if action == "get_transcript":
            return self._get_transcript(**kwargs)
        elif action == "analyze_video":
            return self._analyze_video(**kwargs)
        elif action == "get_metadata":
            return self._get_metadata(**kwargs)
        else:
            return self._get_transcript(**kwargs)  # Default to transcript
    
    def _call_ytmcp(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the ytmcp MCP server directly.
        
        Args:
            tool_name: Name of the ytmcp tool to call
            args: Arguments for the tool
            
        Returns:
            Dictionary with results from ytmcp server
        """
        try:
            # Prepare the command to call ytmcp
            cmd = [sys.executable, "-m", "ytmcp", "--tool", tool_name, "--args", json.dumps(args)]
            
            # Execute the command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {
                    "error": f"ytmcp call failed: {result.stderr}",
                    "tool": tool_name,
                    "args": args
                }
                
        except subprocess.TimeoutExpired:
            return {
                "error": "ytmcp call timed out",
                "tool": tool_name,
                "args": args
            }
        except Exception as e:
            return {
                "error": f"Failed to call ytmcp: {str(e)}",
                "tool": tool_name,
                "args": args
            }
    
    def _get_transcript(self, video_url: str, language: str = "en") -> str:
        """
        Get transcript for a YouTube video.
        
        Args:
            video_url: YouTube video URL
            language: Language code for transcript (default: en)
            
        Returns:
            JSON string with transcript data
        """
        
        args = {
            "video_url": video_url,
            "language": language
        }
        
        result = self._call_ytmcp("get_transcript", args)
        
        # If successful, enhance with basic analysis
        if "error" not in result and "transcript" in result:
            transcript_text = result.get("transcript", "")
            
            # Add basic analysis
            result["analysis"] = {
                "word_count": len(transcript_text.split()),
                "estimated_reading_time": f"{len(transcript_text.split()) // 200} minutes",
                "has_content": bool(transcript_text.strip())
            }
        
        return json.dumps(result, indent=2)
    
    def _analyze_video(self, video_url: str, analysis_type: str = "full") -> str:
        """
        Analyze YouTube video content by first getting transcript then analyzing.
        
        Args:
            video_url: YouTube video URL to analyze
            analysis_type: Type of analysis (full, themes, insights)
            
        Returns:
            JSON string with analysis results
        """
        
        # First get the transcript
        transcript_result = self._call_ytmcp("get_transcript", {"video_url": video_url})
        
        if "error" in transcript_result:
            return json.dumps(transcript_result, indent=2)
        
        transcript_text = transcript_result.get("transcript", "")
        
        # Perform basic analysis on the transcript
        analysis = {
            "video_url": video_url,
            "analysis_type": analysis_type,
            "transcript_available": bool(transcript_text.strip()),
            "word_count": len(transcript_text.split()),
            "estimated_duration": transcript_result.get("duration", "Unknown"),
            "language": transcript_result.get("language", "en")
        }
        
        if transcript_text.strip():
            # Basic keyword/theme extraction
            common_words = self._extract_keywords(transcript_text)
            analysis["themes"] = common_words[:10]  # Top 10 keywords as themes
            
            # Basic insights
            analysis["insights"] = self._generate_insights(transcript_text)
        
        # Combine transcript and analysis
        result = {
            "transcript_data": transcript_result,
            "analysis": analysis
        }
        
        return json.dumps(result, indent=2)
    
    def _get_metadata(self, video_url: str) -> str:
        """
        Get video metadata via ytmcp.
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            JSON string with metadata
        """
        
        args = {"video_url": video_url}
        result = self._call_ytmcp("get_metadata", args)
        
        return json.dumps(result, indent=2)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from transcript text.
        
        Args:
            text: Transcript text
            
        Returns:
            List of keywords
        """
        # Simple keyword extraction
        import re
        from collections import Counter
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your',
            'his', 'her', 'its', 'our', 'their', 'so', 'if', 'when', 'where', 'why', 'how', 'what', 'who'
        }
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter out stop words and short words
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Count frequency
        word_counts = Counter(filtered_words)
        
        # Return top keywords
        return [word for word, count in word_counts.most_common(20)]
    
    def _generate_insights(self, text: str) -> List[str]:
        """
        Generate basic insights from transcript.
        
        Args:
            text: Transcript text
            
        Returns:
            List of insights
        """
        insights = []
        
        # Content length insight
        word_count = len(text.split())
        if word_count > 1000:
            insights.append("Long-form content - suitable for detailed analysis")
        elif word_count > 500:
            insights.append("Medium-length content - good for topic exploration")
        else:
            insights.append("Short content - likely focused on specific topic")
        
        # Question detection
        question_count = text.count('?')
        if question_count > 5:
            insights.append("Interactive content with audience engagement")
        
        # Instructional content detection
        instructional_keywords = ['how to', 'step by step', 'tutorial', 'guide', 'learn', 'teaching']
        if any(keyword in text.lower() for keyword in instructional_keywords):
            insights.append("Educational/instructional content detected")
        
        # Travel/adventure content detection
        travel_keywords = ['travel', 'adventure', 'explore', 'journey', 'visit', 'destination']
        if any(keyword in text.lower() for keyword in travel_keywords):
            insights.append("Travel/adventure content - suitable for experience planning")
        
        return insights 