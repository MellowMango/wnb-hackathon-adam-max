#!/usr/bin/env python3
"""
Setup script for YouTube Playlist Monitor

This script helps users set up the YouTube playlist monitor with proper configuration.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create a .env file with template configuration."""
    env_content = """# YouTube Playlist Monitor Configuration

# Required: Your YouTube Data API key
# Get it from: https://console.cloud.google.com/
YOUTUBE_API_KEY=your_youtube_api_key_here

# Required: YouTube playlist ID to monitor
# Extract from playlist URL: https://www.youtube.com/playlist?list=PLxxxxxxxxxx
PLAYLIST_ID=your_playlist_id_here

# Optional: Check interval in seconds (default: 300 = 5 minutes)
CHECK_INTERVAL=300

# Optional: Output directory for extracted data (default: youtube_data)
OUTPUT_DIRECTORY=youtube_data

# Optional: Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
"""
    
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping creation.")
        return False
    
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print("✅ Created .env file with template configuration")
    print("📝 Please edit .env file with your actual API key and playlist ID")
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'googleapiclient',
        'youtube_transcript_api',
        'requests',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'googleapiclient':
                import googleapiclient.discovery
            elif package == 'youtube_transcript_api':
                import youtube_transcript_api
            elif package == 'requests':
                import requests
            elif package == 'python-dotenv':
                import dotenv
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def print_instructions():
    """Print setup instructions."""
    print("\n" + "="*60)
    print("🎬 YouTube Playlist Monitor - Setup Instructions")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Edit the .env file with your YouTube API key and playlist ID")
    print("2. Get your YouTube API key from: https://console.cloud.google.com/")
    print("3. Get your playlist ID from the YouTube playlist URL")
    print("4. Run the monitor: python main.py")
    
    print("\n🔧 Configuration:")
    print("- Edit .env file to customize settings")
    print("- Use --help for command-line options")
    print("- Check README.md for detailed documentation")
    
    print("\n📁 Project Structure:")
    print("- src/: Core monitoring functionality")
    print("- config/: Configuration management")
    print("- examples/: Usage examples")
    print("- tests/: Unit tests")
    
    print("\n🚀 Quick Start:")
    print("python main.py --help")
    print("python main.py --one-time  # Test run")
    print("python main.py             # Start monitoring")

def main():
    """Main setup function."""
    print("🎬 YouTube Playlist Monitor - Setup")
    print("="*40)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    deps_ok = check_dependencies()
    
    # Create .env file
    print("\n📝 Creating configuration file...")
    env_created = create_env_file()
    
    # Print instructions
    print_instructions()
    
    if not deps_ok:
        print("\n❌ Setup incomplete - please install missing dependencies")
        return False
    
    print("\n✅ Setup completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 