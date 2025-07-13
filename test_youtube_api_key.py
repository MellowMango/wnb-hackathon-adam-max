#!/usr/bin/env python3
"""
Test YouTube API Key

Quick test to verify your YouTube Data API key works.
"""

import os
import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def test_api_key(api_key: str):
    """Test if the YouTube API key works."""
    print(f"🔑 Testing API key: {api_key[:10]}...")
    
    try:
        # Initialize YouTube API
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Simple test query - get channel info for YouTube's own channel
        request = youtube.channels().list(
            part="snippet",
            forUsername="YouTube"
        )
        response = request.execute()
        
        print("✅ API key is valid!")
        print(f"📊 API quota used: ~1 unit")
        print(f"🔍 Test query successful")
        
        return True
        
    except HttpError as e:
        print(f"❌ API key test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """Main function to test API key."""
    
    # Get API key from environment or command line
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key or api_key.startswith('your-'):
        if len(sys.argv) > 1:
            api_key = sys.argv[1]
        else:
            print("❌ YouTube API Key needed!")
            print("   Usage: python test_youtube_api_key.py YOUR_API_KEY")
            print("   Or set: export YOUTUBE_API_KEY='your_key'")
            return
    
    print("🧪 YouTube API Key Test")
    print("=" * 30)
    
    if test_api_key(api_key):
        print("\n🎉 Your API key is working!")
        print("📋 You can now run the playlist extractor:")
        print(f"   python youtube_data_api_extractor.py {api_key[:10]}...")
    else:
        print("\n🛠️  Please check your API key:")
        print("   1. Make sure it's a valid YouTube Data API v3 key")
        print("   2. Enable the YouTube Data API v3 in Google Console")
        print("   3. Check API quotas and restrictions")
        print("   4. Get your key from: https://console.cloud.google.com/apis/credentials")


if __name__ == "__main__":
    main() 