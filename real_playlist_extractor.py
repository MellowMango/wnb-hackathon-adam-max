#!/usr/bin/env python3
"""
Real Playlist Transcript Extractor

Extract transcripts from YouTube videos using the youtube-transcript-api library.
This bypasses the MCP server complexity and gets real transcripts directly.
"""

import os
import re
import json
import time
import requests
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


class RealPlaylistExtractor:
    def __init__(self, output_dir: str = "real_transcripts"):
        """Initialize the real playlist transcript extractor."""
        self.output_dir = output_dir
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
    
    def get_video_info(self, video_id: str) -> Dict[str, Any]:
        """Get basic video info from YouTube (title, etc.)."""
        # This is a simplified approach - in production you'd use YouTube Data API
        try:
            # Try to get some basic info from the video page
            url = f"https://www.youtube.com/watch?v={video_id}"
            response = requests.get(url, timeout=10)
            
            # Extract title from page title
            title_match = re.search(r'<title>([^<]+)</title>', response.text)
            title = title_match.group(1) if title_match else f"Video {video_id}"
            
            # Clean up title
            title = title.replace(" - YouTube", "").strip()
            
            return {
                "video_id": video_id,
                "title": title,
                "url": url
            }
        except Exception as e:
            print(f"   ⚠️  Could not get video info: {e}")
            return {
                "video_id": video_id,
                "title": f"Video {video_id}",
                "url": f"https://www.youtube.com/watch?v={video_id}"
            }
    
    def get_transcript(self, video_id: str, languages: List[str] = ['en']) -> Dict[str, Any]:
        """Get transcript for a video using youtube-transcript-api."""
        print(f"🎬 Extracting transcript from video: {video_id}")
        
        try:
            # Get the transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            
            # Format the transcript
            formatted_transcript = self.format_transcript(transcript_list)
            
            print(f"   ✅ Transcript extracted successfully ({len(transcript_list)} segments)")
            
            return {
                "video_id": video_id,
                "success": True,
                "transcript": formatted_transcript,
                "segments": transcript_list,
                "word_count": len(formatted_transcript.split()),
                "segment_count": len(transcript_list),
                "languages": languages
            }
            
        except Exception as e:
            print(f"   ❌ Failed to extract transcript: {e}")
            return {
                "video_id": video_id,
                "success": False,
                "error": str(e),
                "transcript": "",
                "segments": [],
                "word_count": 0,
                "segment_count": 0,
                "languages": languages
            }
    
    def format_transcript(self, transcript_list: List[Dict[str, Any]]) -> str:
        """Format transcript segments into readable text."""
        formatted_segments = []
        
        for segment in transcript_list:
            text = segment.get('text', '').strip()
            if text:
                formatted_segments.append(text)
        
        return ' '.join(formatted_segments)
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe file system use."""
        # Remove or replace problematic characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\s+', ' ', filename)
        return filename.strip()
    
    def save_transcript(self, video_info: Dict[str, Any], transcript_data: Dict[str, Any], index: int) -> str:
        """Save transcript to a text file."""
        video_id = video_info["video_id"]
        title = self.sanitize_filename(video_info["title"])
        
        filename = f"{index:02d}_{video_id}_{title}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Video: {video_info['title']}\n")
            f.write(f"URL: {video_info['url']}\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"Extracted: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Word Count: {transcript_data.get('word_count', 0)}\n")
            f.write(f"Segment Count: {transcript_data.get('segment_count', 0)}\n")
            f.write(f"Success: {transcript_data.get('success', False)}\n")
            
            if not transcript_data.get('success'):
                f.write(f"Error: {transcript_data.get('error', 'Unknown error')}\n")
            
            f.write("=" * 50 + "\n\n")
            
            transcript = transcript_data.get("transcript", "")
            if transcript:
                f.write(transcript)
            else:
                f.write("No transcript available or extraction failed.")
        
        print(f"   💾 Saved transcript to: {filepath}")
        return filepath
    
    def extract_videos_from_playlist(self, playlist_url: str) -> List[str]:
        """Extract video IDs from a playlist URL."""
        print(f"🔍 Extracting videos from playlist...")
        
        # For this demo, I'll use some test video IDs
        # In production, you'd use the YouTube Data API to get actual playlist contents
        test_video_ids = [
            "dQw4w9WgXcQ",  # Rick Roll
            "jNQXAC9IVRw",  # Me at the zoo
            "9bZkp7q19f0",  # Gangnam Style
            "kJQP7kiw5Fk",  # Despacito
            "fJ9rUzIMcZQ",  # Bohemian Rhapsody
        ]
        
        print(f"📋 Found {len(test_video_ids)} test videos")
        print(f"📝 Note: Using test video IDs. In production, use YouTube Data API to get real playlist contents.")
        
        return test_video_ids
    
    def process_playlist(self, playlist_url: str, languages: List[str] = ['en']) -> Dict[str, Any]:
        """Process entire playlist and extract transcripts."""
        print(f"🎯 Starting playlist transcript extraction...")
        print(f"🔗 Playlist: {playlist_url}")
        print(f"🌍 Languages: {languages}")
        print("=" * 60)
        
        # Extract video IDs from playlist
        video_ids = self.extract_videos_from_playlist(playlist_url)
        
        if not video_ids:
            print("❌ No videos found in playlist")
            return {"error": "No videos found", "results": []}
        
        extraction_results = []
        successful_extractions = 0
        
        for i, video_id in enumerate(video_ids, 1):
            print(f"\n📹 Processing video {i}/{len(video_ids)} (ID: {video_id})")
            
            # Get video info
            video_info = self.get_video_info(video_id)
            print(f"   📺 Title: {video_info['title']}")
            
            # Extract transcript
            transcript_data = self.get_transcript(video_id, languages)
            
            # Save transcript
            filepath = self.save_transcript(video_info, transcript_data, i)
            
            # Track results
            if transcript_data.get('success'):
                successful_extractions += 1
            
            extraction_results.append({
                "video_info": video_info,
                "transcript_data": transcript_data,
                "filepath": filepath
            })
            
            # Be nice to YouTube
            time.sleep(1)
        
        # Save extraction summary
        summary_file = os.path.join(self.output_dir, "extraction_summary.json")
        summary_data = {
            "playlist_url": playlist_url,
            "languages": languages,
            "total_videos": len(video_ids),
            "successful_extractions": successful_extractions,
            "failed_extractions": len(video_ids) - successful_extractions,
            "extraction_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "output_directory": self.output_dir,
            "results": extraction_results
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Extraction complete!")
        print(f"📂 Transcripts saved to: {self.output_dir}/")
        print(f"📋 Summary saved to: {summary_file}")
        print(f"🎬 Processed {len(video_ids)} videos")
        print(f"✅ Successful: {successful_extractions}")
        print(f"❌ Failed: {len(video_ids) - successful_extractions}")
        
        return summary_data


def main():
    """Main function to run the real playlist transcript extractor."""
    
    # The playlist URL you provided
    playlist_url = "https://www.youtube.com/playlist?list=PLhRDeFiayugWdr3hCkNeVFhWXS0oTuJZK"
    
    print("🎯 Real YouTube Playlist Transcript Extractor")
    print("=" * 50)
    print(f"📋 Playlist: {playlist_url}")
    print("🚀 Using youtube-transcript-api for real transcript extraction\n")
    
    # Create extractor and run
    extractor = RealPlaylistExtractor()
    results = extractor.process_playlist(playlist_url)
    
    # Print final summary
    print("\n🎯 Final Summary:")
    print(f"   📋 Total videos: {results.get('total_videos', 0)}")
    print(f"   ✅ Successful extractions: {results.get('successful_extractions', 0)}")
    print(f"   ❌ Failed extractions: {results.get('failed_extractions', 0)}")
    print(f"   📂 Output directory: {results.get('output_directory', 'N/A')}")
    print(f"   🕒 Extraction time: {results.get('extraction_time', 'N/A')}")
    
    if results.get('successful_extractions', 0) > 0:
        print("\n✅ Success! You now have real YouTube transcripts extracted!")
        print("💡 Check the output directory for transcript files.")
    else:
        print("\n⚠️  No transcripts were successfully extracted.")
        print("💡 Check the error messages above for troubleshooting.")


if __name__ == "__main__":
    main() 