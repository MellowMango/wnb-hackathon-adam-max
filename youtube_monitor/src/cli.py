#!/usr/bin/env python3
"""
YouTube Playlist Monitor - Command Line Interface

This module provides the command-line interface for the YouTube playlist monitor.
"""

import sys
import argparse
import logging
from pathlib import Path

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent))

from monitor import YouTubePlaylistMonitor

def main():
    """Main function to run the YouTube playlist monitor."""
    
    parser = argparse.ArgumentParser(
        description='Monitor YouTube playlist for new videos and extract transcriptions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with environment variables
  python cli.py

  # Run with command line arguments
  python cli.py --api-key YOUR_KEY --playlist-id YOUR_PLAYLIST_ID

  # Run once without continuous monitoring
  python cli.py --one-time

  # Custom check interval (10 minutes)
  python cli.py --check-interval 600
        """
    )
    
    parser.add_argument(
        '--api-key',
        help='YouTube Data API key (or set YOUTUBE_API_KEY env var)'
    )
    parser.add_argument(
        '--playlist-id',
        help='YouTube playlist ID (or set PLAYLIST_ID env var)'
    )
    parser.add_argument(
        '--output-dir',
        default='youtube_data',
        help='Output directory for extracted data (default: youtube_data)'
    )
    parser.add_argument(
        '--check-interval',
        type=int,
        default=300,
        help='Check interval in seconds (default: 300)'
    )
    parser.add_argument(
        '--one-time',
        action='store_true',
        help='Run once and exit (don\'t monitor continuously)'
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
    
    # Get API key and playlist ID
    api_key = args.api_key or get_env_var('YOUTUBE_API_KEY')
    playlist_id = args.playlist_id or get_env_var('PLAYLIST_ID')
    
    if not api_key:
        print("❌ Error: YouTube API key not found")
        print("Please set YOUTUBE_API_KEY environment variable or use --api-key")
        sys.exit(1)
    
    if not playlist_id:
        print("❌ Error: Playlist ID not found")
        print("Please set PLAYLIST_ID environment variable or use --playlist-id")
        sys.exit(1)
    
    # Print configuration
    print("🎬 YouTube Playlist Monitor")
    print("=" * 40)
    print(f"Playlist ID: {playlist_id}")
    print(f"Output Directory: {args.output_dir}")
    print(f"Check Interval: {args.check_interval} seconds")
    print(f"Mode: {'One-time' if args.one_time else 'Continuous'}")
    print("=" * 40)
    
    # Create and run monitor
    try:
        monitor = YouTubePlaylistMonitor(
            api_key=api_key,
            playlist_id=playlist_id,
            output_dir=args.output_dir
        )
        
        if args.one_time:
            # Run once
            new_videos = monitor.check_for_new_videos()
            if new_videos:
                print(f"Found {len(new_videos)} new video(s)")
                for video in new_videos:
                    print(f"Processing: {video['title']}")
                    monitor.process_video(video)
            else:
                print("No new videos found")
        else:
            # Monitor continuously
            print("Press Ctrl+C to stop monitoring")
            monitor.monitor_playlist(check_interval=args.check_interval)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"Error during monitoring: {e}")
        sys.exit(1)

def get_env_var(name: str) -> str:
    """Get environment variable value."""
    import os
    return os.getenv(name, '')

if __name__ == "__main__":
    main() 