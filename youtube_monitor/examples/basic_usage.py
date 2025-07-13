#!/usr/bin/env python3
"""
Basic usage example for YouTube Video Monitor

This example shows how to use the YouTube Video Monitor to process
individual videos and extract their metadata and transcripts.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from monitor import YouTubeVideoMonitor, extract_video_id

def main():
    """Basic usage example."""
    
    # Configuration
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        print("❌ Error: Please set YOUTUBE_API_KEY environment variable")
        return
    
    # Example video URLs
    video_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up
        "https://youtu.be/dQw4w9WgXcQ",                 # Short URL format
        "dQw4w9WgXcQ",                                  # Just the video ID
    ]
    
    # Create monitor
    monitor = YouTubeVideoMonitor(
        api_key=api_key,
        output_dir="example_output"
    )
    
    print("🎬 YouTube Video Monitor - Basic Usage Example")
    print("=" * 50)
    
    # Process each video
    for url in video_urls:
        print(f"\n📺 Processing: {url}")
        
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            print(f"❌ Invalid URL: {url}")
            continue
        
        print(f"   Video ID: {video_id}")
        
        # Process video
        try:
            video_dir = monitor.process_video(url)
            
            if video_dir:
                print(f"✅ Successfully processed!")
                print(f"   Data saved to: {video_dir}")
                
                # Show what files were created
                files = list(video_dir.glob("*"))
                for file in files:
                    print(f"   - {file.name}")
            else:
                print(f"❌ Failed to process video")
                
        except Exception as e:
            print(f"❌ Error processing video: {e}")
    
    print("\n🎉 Example completed!")
    print("Check the 'example_output' directory for extracted data.")

if __name__ == "__main__":
    main() 