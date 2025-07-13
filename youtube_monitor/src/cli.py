#!/usr/bin/env python3
"""
YouTube Video Monitor - Command Line Interface

This module provides the command-line interface for the YouTube video monitor.
"""

import sys
import argparse
import logging
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, skip loading .env file
    pass

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent))

from monitor import YouTubeVideoMonitor, extract_video_id

def main():
    """Main function to run the YouTube video monitor."""
    
    parser = argparse.ArgumentParser(
        description='Extract transcriptions and metadata from YouTube videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a video with environment variables
  python cli.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

  # Process a video with API key
  python cli.py --api-key YOUR_KEY https://youtu.be/dQw4w9WgXcQ

  # Process with custom output directory
  python cli.py --output-dir my_videos https://www.youtube.com/watch?v=dQw4w9WgXcQ

  # Process with just video ID
  python cli.py dQw4w9WgXcQ
        """
    )
    
    parser.add_argument(
        'video_url',
        help='YouTube video URL or video ID'
    )
    parser.add_argument(
        '--api-key',
        help='YouTube Data API key (or set YOUTUBE_API_KEY env var)'
    )
    parser.add_argument(
        '--output-dir',
        default='youtube_data',
        help='Output directory for extracted data (default: youtube_data)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Get API key
    api_key = args.api_key or get_env_var('YOUTUBE_API_KEY')
    
    if not api_key:
        print("❌ Error: YouTube API key not found")
        print("Please set YOUTUBE_API_KEY environment variable or use --api-key")
        sys.exit(1)
    
    # Validate video URL/ID
    video_id = extract_video_id(args.video_url)
    if not video_id:
        print(f"❌ Error: Invalid YouTube video URL or ID: {args.video_url}")
        print("Please provide a valid YouTube video URL or 11-character video ID")
        sys.exit(1)
    
    # Print configuration
    print("🎬 YouTube Video Monitor")
    print("=" * 40)
    print(f"Video URL/ID: {args.video_url}")
    print(f"Video ID: {video_id}")
    print(f"Output Directory: {args.output_dir}")
    print("=" * 40)
    
    # Create and run monitor
    try:
        monitor = YouTubeVideoMonitor(
            api_key=api_key,
            output_dir=args.output_dir
        )
        
        # Process the video
        video_dir = monitor.process_video(args.video_url)
        
        if video_dir:
            print(f"✅ Successfully processed video!")
            print(f"📁 Data saved to: {video_dir}")
            print(f"   - metadata.json: Video metadata")
            print(f"   - transcript.txt: Full transcript")
            print(f"   - summary.txt: Video summary")
        else:
            print("❌ Failed to process video")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Processing stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"Error during processing: {e}")
        sys.exit(1)

def get_env_var(name: str) -> str:
    """Get environment variable value."""
    import os
    return os.getenv(name, '')

if __name__ == "__main__":
    main() 