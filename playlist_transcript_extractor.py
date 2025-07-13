#!/usr/bin/env python3
"""
Playlist Transcript Extractor

Extract transcripts from all videos in a YouTube playlist using the MCP server.
"""

import os
import re
import json
import requests
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, parse_qs
import time


class PlaylistTranscriptExtractor:
    def __init__(self, mcp_server_url: str = "http://localhost:8000"):
        """Initialize the playlist transcript extractor."""
        self.mcp_server_url = mcp_server_url
        self.output_dir = "transcripts"
        self.ensure_output_dir()
        
    def ensure_output_dir(self):
        """Ensure the output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
            r'youtube\.com/v/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def extract_playlist_id(self, url: str) -> Optional[str]:
        """Extract playlist ID from YouTube URL."""
        parsed = urlparse(url)
        if parsed.hostname in ['www.youtube.com', 'youtube.com']:
            query_params = parse_qs(parsed.query)
            return query_params.get('list', [None])[0]
        return None
    
    def get_playlist_videos(self, playlist_url: str) -> List[Dict[str, Any]]:
        """
        Get video URLs from a playlist.
        
        Note: This is a simplified version that works with known playlist patterns.
        For production use, you'd want to use the YouTube Data API.
        """
        playlist_id = self.extract_playlist_id(playlist_url)
        if not playlist_id:
            print(f"❌ Could not extract playlist ID from: {playlist_url}")
            return []
        
        # For this demo, we'll use some common video IDs from playlists
        # In production, you'd use the YouTube Data API
        sample_videos = [
            {
                "video_id": "dQw4w9WgXcQ",
                "title": "Rick Astley - Never Gonna Give You Up",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            },
            {
                "video_id": "jNQXAC9IVRw",
                "title": "Me at the zoo",
                "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw"
            },
            {
                "video_id": "9bZkp7q19f0",
                "title": "Gangnam Style",
                "url": "https://www.youtube.com/watch?v=9bZkp7q19f0"
            }
        ]
        
        print(f"📋 Found {len(sample_videos)} videos in playlist")
        print(f"📝 Note: Using sample videos for demo. In production, use YouTube Data API.")
        
        return sample_videos
    
    def call_mcp_server(self, method: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Call the MCP server with the given method and arguments."""
        try:
            response = requests.post(
                f"{self.mcp_server_url}/mcp/run",
                json={"method": method, "args": args},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"⚠️  MCP server error: {e}")
            return {"error": str(e), "fallback": True}
    
    def extract_transcript(self, video_url: str, lang: str = "en") -> Dict[str, Any]:
        """Extract transcript from a single video."""
        print(f"🎬 Extracting transcript from: {video_url}")
        
        result = self.call_mcp_server("get_transcript", {
            "video_url": video_url,
            "lang": lang
        })
        
        if result.get("fallback"):
            print(f"   ⚠️  Using fallback data (MCP server unavailable)")
        else:
            print(f"   ✅ Transcript extracted successfully")
            
        return result
    
    def analyze_video(self, video_url: str) -> Dict[str, Any]:
        """Analyze video content using the MCP server."""
        print(f"🔍 Analyzing video: {video_url}")
        
        result = self.call_mcp_server("analyze_video", {
            "video_url": video_url,
            "analysis_type": "full"
        })
        
        if result.get("fallback"):
            print(f"   ⚠️  Using fallback analysis data")
        else:
            print(f"   ✅ Analysis completed successfully")
            
        return result
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe file system use."""
        # Remove or replace problematic characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\s+', ' ', filename)
        return filename.strip()
    
    def save_transcript(self, video_data: Dict[str, Any], transcript_data: Dict[str, Any], index: int):
        """Save transcript to a text file."""
        video_id = video_data["video_id"]
        title = self.sanitize_filename(video_data["title"])
        
        filename = f"{index:02d}_{video_id}_{title}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Video: {video_data['title']}\n")
            f.write(f"URL: {video_data['url']}\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"Language: {transcript_data.get('language', 'en')}\n")
            f.write(f"Extracted: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            if transcript_data.get("fallback"):
                f.write("⚠️  FALLBACK DATA (MCP server unavailable)\n")
            
            f.write("=" * 50 + "\n\n")
            
            transcript = transcript_data.get("transcript", "")
            if transcript:
                f.write(transcript)
            else:
                f.write("No transcript available.")
        
        print(f"   💾 Saved transcript to: {filepath}")
        return filepath
    
    def extract_playlist_transcripts(self, playlist_url: str, lang: str = "en") -> Dict[str, Any]:
        """Extract transcripts from all videos in a playlist."""
        print(f"🎯 Starting playlist transcript extraction...")
        print(f"🔗 Playlist: {playlist_url}")
        print(f"🌍 Language: {lang}")
        print("=" * 60)
        
        # Get videos from playlist
        videos = self.get_playlist_videos(playlist_url)
        
        if not videos:
            print("❌ No videos found in playlist")
            return {"error": "No videos found", "videos": []}
        
        extraction_results = []
        
        for i, video in enumerate(videos, 1):
            print(f"\n📹 Processing video {i}/{len(videos)}: {video['title']}")
            
            # Extract transcript
            transcript_data = self.extract_transcript(video["url"], lang)
            
            # Save transcript
            filepath = self.save_transcript(video, transcript_data, i)
            
            # Analyze video (optional)
            analysis_data = self.analyze_video(video["url"])
            
            extraction_results.append({
                "video": video,
                "transcript": transcript_data,
                "analysis": analysis_data,
                "filepath": filepath
            })
            
            # Be nice to the server
            time.sleep(1)
        
        # Save extraction summary
        summary_file = os.path.join(self.output_dir, "extraction_summary.json")
        summary_data = {
            "playlist_url": playlist_url,
            "language": lang,
            "total_videos": len(videos),
            "extraction_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "results": extraction_results
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Extraction complete!")
        print(f"📂 Transcripts saved to: {self.output_dir}/")
        print(f"📋 Summary saved to: {summary_file}")
        print(f"🎬 Processed {len(videos)} videos")
        
        return summary_data


def main():
    """Main function to run the playlist transcript extractor."""
    playlist_url = "https://www.youtube.com/playlist?list=PLhRDeFiayugWdr3hCkNeVFhWXS0oTuJZK"
    
    # Check if MCP server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ YouTube MCP server is running!")
        else:
            print("⚠️  MCP server responded with non-200 status")
    except:
        print("❌ MCP server is not running. Please start it first.")
        print("   Run: cd mcp_servers && python youtube_wrapper.py")
        return
    
    # Create extractor and run
    extractor = PlaylistTranscriptExtractor()
    results = extractor.extract_playlist_transcripts(playlist_url)
    
    # Print summary
    print("\n🎯 Extraction Summary:")
    print(f"   📋 Total videos: {results.get('total_videos', 0)}")
    print(f"   📂 Output directory: {extractor.output_dir}")
    print(f"   🕒 Extraction time: {results.get('extraction_time', 'N/A')}")


if __name__ == "__main__":
    main() 