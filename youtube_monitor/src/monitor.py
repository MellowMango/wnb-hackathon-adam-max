#!/usr/bin/env python3
"""
YouTube Playlist Monitor - Core Monitoring Module

This module provides the main functionality for monitoring YouTube playlists
and extracting video transcriptions and metadata.
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

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

class YouTubePlaylistMonitor:
    """Main class for monitoring YouTube playlists and extracting video data."""
    
    def __init__(self, api_key: str, playlist_id: str, output_dir: str = "youtube_data"):
        """
        Initialize the YouTube playlist monitor.
        
        Args:
            api_key: YouTube Data API key
            playlist_id: YouTube playlist ID
            output_dir: Directory to save extracted data
        """
        self.api_key = api_key
        self.playlist_id = playlist_id
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize YouTube API client
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Track processed videos
        self.processed_videos_file = self.output_dir / "processed_videos.json"
        self.processed_videos = self._load_processed_videos()
        
        logger.info(f"Initialized monitor for playlist: {playlist_id}")
        logger.info(f"Output directory: {self.output_dir}")
    
    def _load_processed_videos(self) -> set:
        """Load list of already processed video IDs."""
        if self.processed_videos_file.exists():
            try:
                with open(self.processed_videos_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('processed_videos', []))
            except Exception as e:
                logger.error(f"Error loading processed videos: {e}")
        return set()
    
    def _save_processed_videos(self):
        """Save list of processed video IDs."""
        try:
            with open(self.processed_videos_file, 'w') as f:
                json.dump({
                    'processed_videos': list(self.processed_videos),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving processed videos: {e}")
    
    def get_playlist_videos(self) -> List[Dict[str, Any]]:
        """Get all videos from the playlist."""
        videos = []
        next_page_token = None
        
        try:
            while True:
                request = self.youtube.playlistItems().list(
                    part='snippet,contentDetails',
                    playlistId=self.playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                
                response = request.execute()
                
                for item in response['items']:
                    video_data = {
                        'video_id': item['contentDetails']['videoId'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'published_at': item['snippet']['publishedAt'],
                        'channel_title': item['snippet']['channelTitle'],
                        'playlist_position': item['snippet']['position']
                    }
                    videos.append(video_data)
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                    
        except HttpError as e:
            logger.error(f"Error fetching playlist videos: {e}")
        
        return videos
    
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
    
    def check_for_new_videos(self) -> List[Dict[str, Any]]:
        """Check for new videos in the playlist."""
        logger.info("Checking for new videos in playlist...")
        
        videos = self.get_playlist_videos()
        new_videos = []
        
        for video in videos:
            video_id = video['video_id']
            if video_id not in self.processed_videos:
                new_videos.append(video)
                logger.info(f"Found new video: {video['title']} ({video_id})")
        
        return new_videos
    
    def process_video(self, video_data: Dict[str, Any]):
        """Process a single video: get metadata, transcript, and save data."""
        video_id = video_data['video_id']
        
        logger.info(f"Processing video: {video_data['title']} ({video_id})")
        
        # Get detailed metadata
        metadata = self.get_video_metadata(video_id)
        if not metadata:
            logger.error(f"Could not get metadata for video {video_id}")
            return
        
        # Get transcript
        transcript = self.get_video_transcript(video_id)
        
        # Save all data
        self.save_video_data(video_id, metadata, transcript)
        
        # Mark as processed
        self.processed_videos.add(video_id)
        self._save_processed_videos()
        
        logger.info(f"Successfully processed video {video_id}")
    
    def monitor_playlist(self, check_interval: int = 300):
        """
        Continuously monitor the playlist for new videos.
        
        Args:
            check_interval: Time between checks in seconds (default: 5 minutes)
        """
        logger.info(f"Starting playlist monitoring. Checking every {check_interval} seconds...")
        
        try:
            while True:
                new_videos = self.check_for_new_videos()
                
                if new_videos:
                    logger.info(f"Found {len(new_videos)} new video(s)")
                    for video in new_videos:
                        self.process_video(video)
                else:
                    logger.info("No new videos found")
                
                logger.info(f"Next check in {check_interval} seconds...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error during monitoring: {e}")
            raise 