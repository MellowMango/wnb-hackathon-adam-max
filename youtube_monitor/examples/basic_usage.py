#!/usr/bin/env python3
"""
Basic Usage Example

This example shows how to use the YouTube Playlist Monitor
with minimal configuration.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from monitor import YouTubePlaylistMonitor

def main():
    """Basic usage example."""
    
    # Configuration - replace with your actual values
    API_KEY = "your_youtube_api_key_here"
    PLAYLIST_ID = "your_playlist_id_here"
    
    print("🎬 Basic Usage Example")
    print("=" * 40)
    
    # Create monitor instance
    monitor = YouTubePlaylistMonitor(
        api_key=API_KEY,
        playlist_id=PLAYLIST_ID,
        output_dir="example_output"
    )
    
    # Check for new videos once
    print("Checking for new videos...")
    new_videos = monitor.check_for_new_videos()
    
    if new_videos:
        print(f"Found {len(new_videos)} new video(s)")
        for video in new_videos:
            print(f"Processing: {video['title']}")
            monitor.process_video(video)
    else:
        print("No new videos found")
    
    print("✅ Example completed!")

if __name__ == "__main__":
    main() 