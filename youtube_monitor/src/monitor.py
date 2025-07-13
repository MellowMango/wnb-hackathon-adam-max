#!/usr/bin/env python3
"""
YouTube Video Monitor - Core Monitoring Module

This module provides the main functionality for monitoring YouTube videos/playlists
and extracting video transcriptions and metadata.
"""

import os
import json
import time
import logging
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('youtube_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from various YouTube URL formats.
    
    Args:
        url: YouTube URL or video ID
        
    Returns:
        Video ID if valid, None otherwise
    """
    # Parse different YouTube URL formats first
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})',
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If it's already a video ID (11 characters, alphanumeric and dashes/underscores)
    # and contains typical YouTube video ID patterns (not just any 11-character string)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url) and not url.lower().startswith('invalid'):
        return url
    
    return None

class YouTubeVideoMonitor:
    """Class for monitoring individual YouTube videos and extracting video data."""
    
    def __init__(self, api_key: str, output_dir: str = "youtube_data"):
        """
        Initialize the YouTube video monitor.
        
        Args:
            api_key: YouTube Data API key
            output_dir: Directory to save extracted data
        """
        self.api_key = api_key
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize YouTube API client
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
        logger.info("Initialized YouTube video monitor")
        logger.info(f"Output directory: {self.output_dir}")
    
    def get_video_metadata(self, video_id: str) -> Dict[str, Any]:
        """Get detailed metadata for a specific video."""
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                video = response['items'][0]
                return {
                    'video_id': video_id,
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'published_at': video['snippet']['publishedAt'],
                    'channel_title': video['snippet']['channelTitle'],
                    'channel_id': video['snippet']['channelId'],
                    'tags': video['snippet'].get('tags', []),
                    'category_id': video['snippet']['categoryId'],
                    'default_language': video['snippet'].get('defaultLanguage'),
                    'duration': video['contentDetails']['duration'],
                    'view_count': video['statistics'].get('viewCount', '0'),
                    'like_count': video['statistics'].get('likeCount', '0'),
                    'comment_count': video['statistics'].get('commentCount', '0'),
                    'favorite_count': video['statistics'].get('favoriteCount', '0'),
                    'definition': video['contentDetails']['definition'],
                    'caption': video['contentDetails']['caption'],
                    'licensed_content': video['contentDetails']['licensedContent'],
                    'projection': video['contentDetails']['projection']
                }
            else:
                logger.error(f"No video found with ID: {video_id}")
                return {}
                
        except HttpError as e:
            logger.error(f"Error fetching video metadata for {video_id}: {e}")
            return {}
    
    def get_video_transcript(self, video_id: str) -> str:
        """Get transcript for a YouTube video."""
        try:
            # Try to get transcript in English first
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            formatter = TextFormatter()
            return formatter.format_transcript(transcript_list)
        except Exception as e:
            try:
                # Try to get transcript in any available language
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                formatter = TextFormatter()
                return formatter.format_transcript(transcript_list)
            except Exception as e2:
                logger.warning(f"Could not get transcript for video {video_id}: {e2}")
                return f"Transcript not available for video {video_id}"
    
    def save_video_data(self, video_id: str, metadata: Dict[str, Any], transcript: str):
        """Save video data to files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create video-specific directory
        video_dir = self.output_dir / f"{video_id}_{timestamp}"
        video_dir.mkdir(exist_ok=True)
        
        # Save metadata
        metadata_file = video_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Save transcript
        transcript_file = video_dir / "transcript.txt"
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(f"Video ID: {video_id}\n")
            f.write(f"Title: {metadata.get('title', 'Unknown')}\n")
            f.write(f"Published: {metadata.get('published_at', 'Unknown')}\n")
            f.write(f"Channel: {metadata.get('channel_title', 'Unknown')}\n")
            f.write(f"Duration: {metadata.get('duration', 'Unknown')}\n")
            f.write(f"Views: {metadata.get('view_count', 'Unknown')}\n")
            f.write(f"Likes: {metadata.get('like_count', 'Unknown')}\n")
            f.write(f"Comments: {metadata.get('comment_count', 'Unknown')}\n")
            f.write("=" * 80 + "\n\n")
            f.write(transcript)
        
        # Save summary
        summary_file = video_dir / "summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"VIDEO SUMMARY\n")
            f.write(f"=" * 50 + "\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"Title: {metadata.get('title', 'Unknown')}\n")
            f.write(f"Channel: {metadata.get('channel_title', 'Unknown')}\n")
            f.write(f"Published: {metadata.get('published_at', 'Unknown')}\n")
            f.write(f"Duration: {metadata.get('duration', 'Unknown')}\n")
            f.write(f"Views: {metadata.get('view_count', 'Unknown')}\n")
            f.write(f"Likes: {metadata.get('like_count', 'Unknown')}\n")
            f.write(f"Comments: {metadata.get('comment_count', 'Unknown')}\n")
            f.write(f"Description: {metadata.get('description', 'No description')[:500]}...\n")
            f.write(f"Tags: {', '.join(metadata.get('tags', []))}\n")
            f.write(f"Transcript Length: {len(transcript)} characters\n")
        
        logger.info(f"Saved data for video {video_id} to {video_dir}")
        return video_dir
    
    def process_video(self, video_url: str) -> Optional[Path]:
        """
        Process a single video: extract ID, get metadata, transcript, and save data.
        
        Args:
            video_url: YouTube video URL or video ID
            
        Returns:
            Path to saved video data directory, or None if processing failed
        """
        video_id = extract_video_id(video_url)
        if not video_id:
            logger.error(f"Could not extract video ID from: {video_url}")
            return None
        
        logger.info(f"Processing video: {video_id}")
        
        # Get detailed metadata
        metadata = self.get_video_metadata(video_id)
        if not metadata:
            logger.error(f"Could not get metadata for video {video_id}")
            return None
        
        logger.info(f"Found video: {metadata['title']}")
        
        # Get transcript
        transcript = self.get_video_transcript(video_id)
        
        # Save all data
        video_dir = self.save_video_data(video_id, metadata, transcript)
        
        logger.info(f"Successfully processed video {video_id}")
        return video_dir 