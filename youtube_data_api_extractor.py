#!/usr/bin/env python3
"""
YouTube Data API Playlist Extractor

Extract playlist videos and transcripts using YouTube Data API v3 directly.
This bypasses the MCP server and gets real data from Google's API.
"""

import os
import json
import time
import re
import sys
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class YouTubeDataAPIExtractor:
    def __init__(self, api_key: str, output_dir: str = "youtube_api_transcripts"):
        """Initialize the YouTube Data API extractor."""
        self.api_key = api_key
        self.output_dir = output_dir
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.ensure_output_dir()
        
    def ensure_output_dir(self):
        """Ensure the output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def extract_playlist_id(self, playlist_url: str) -> Optional[str]:
        """Extract playlist ID from YouTube URL."""
        parsed = urlparse(playlist_url)
        if parsed.hostname in ['www.youtube.com', 'youtube.com']:
            query_params = parse_qs(parsed.query)
            return query_params.get('list', [None])[0]
        return None
    
    def get_playlist_info(self, playlist_id: str) -> Dict[str, Any]:
        """Get playlist information from YouTube Data API."""
        try:
            request = self.youtube.playlists().list(
                part="snippet,contentDetails",
                id=playlist_id
            )
            response = request.execute()
            
            if response['items']:
                playlist = response['items'][0]
                return {
                    'id': playlist['id'],
                    'title': playlist['snippet']['title'],
                    'description': playlist['snippet']['description'],
                    'channel': playlist['snippet']['channelTitle'],
                    'item_count': playlist['contentDetails']['itemCount'],
                    'published_at': playlist['snippet']['publishedAt']
                }
            else:
                return {}
        except HttpError as e:
            print(f"⚠️  Error getting playlist info: {e}")
            return {}
    
    def get_playlist_videos(self, playlist_id: str) -> List[Dict[str, Any]]:
        """Get all videos from a playlist using YouTube Data API."""
        videos = []
        next_page_token = None
        
        print(f"🔍 Fetching videos from playlist: {playlist_id}")
        
        while True:
            try:
                request = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                for item in response['items']:
                    video_id = item['contentDetails']['videoId']
                    snippet = item['snippet']
                    
                    videos.append({
                        'video_id': video_id,
                        'title': snippet['title'],
                        'description': snippet['description'],
                        'channel': snippet['channelTitle'],
                        'published_at': snippet['publishedAt'],
                        'position': snippet['position'],
                        'thumbnail': snippet['thumbnails']['default']['url'],
                        'url': f"https://www.youtube.com/watch?v={video_id}"
                    })
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                    
            except HttpError as e:
                print(f"⚠️  Error fetching playlist videos: {e}")
                break
        
        print(f"📋 Found {len(videos)} videos in playlist")
        return videos
    
    def get_video_details(self, video_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get detailed information for multiple videos."""
        video_details = {}
        
        # Process in batches of 50 (API limit)
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            
            try:
                request = self.youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=','.join(batch_ids)
                )
                response = request.execute()
                
                for video in response['items']:
                    video_id = video['id']
                    snippet = video['snippet']
                    content_details = video['contentDetails']
                    stats = video['statistics']
                    
                    video_details[video_id] = {
                        'title': snippet['title'],
                        'description': snippet['description'],
                        'channel': snippet['channelTitle'],
                        'published_at': snippet['publishedAt'],
                        'duration': content_details['duration'],
                        'view_count': stats.get('viewCount', 0),
                        'like_count': stats.get('likeCount', 0),
                        'comment_count': stats.get('commentCount', 0),
                        'tags': snippet.get('tags', []),
                        'category_id': snippet['categoryId'],
                        'default_language': snippet.get('defaultLanguage', 'en'),
                        'thumbnail': snippet['thumbnails']['high']['url'] if 'high' in snippet['thumbnails'] else snippet['thumbnails']['default']['url']
                    }
                    
            except HttpError as e:
                print(f"⚠️  Error getting video details: {e}")
        
        return video_details
    
    def parse_duration(self, duration_str: str) -> str:
        """Parse ISO 8601 duration to readable format."""
        import re
        
        # PT4M13S -> 4:13
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)
        
        if match:
            hours, minutes, seconds = match.groups()
            hours = int(hours) if hours else 0
            minutes = int(minutes) if minutes else 0
            seconds = int(seconds) if seconds else 0
            
            if hours > 0:
                return f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes}:{seconds:02d}"
        
        return duration_str
    
    def get_transcript(self, video_id: str, languages: List[str] = ['en']) -> Dict[str, Any]:
        """Get transcript for a video using youtube-transcript-api."""
        try:
            # Get the transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            
            # Format the transcript
            formatted_transcript = self.format_transcript(transcript_list)
            
            return {
                'video_id': video_id,
                'success': True,
                'transcript': formatted_transcript,
                'segments': transcript_list,
                'word_count': len(formatted_transcript.split()) if formatted_transcript else 0,
                'segment_count': len(transcript_list),
                'languages': languages
            }
            
        except Exception as e:
            return {
                'video_id': video_id,
                'success': False,
                'error': str(e),
                'transcript': "",
                'segments': [],
                'word_count': 0,
                'segment_count': 0,
                'languages': languages
            }
    
    def format_transcript(self, transcript_list: List[Dict[str, Any]]) -> str:
        """Format transcript segments into readable text."""
        if not transcript_list:
            return ""
            
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
        return filename.strip()[:200]  # Limit length
    
    def save_video_data(self, video_info: Dict[str, Any], video_details: Dict[str, Any], 
                       transcript_data: Dict[str, Any], index: int) -> str:
        """Save video data and transcript to a text file."""
        video_id = video_info["video_id"]
        title = self.sanitize_filename(video_info["title"])
        
        filename = f"{index:02d}_{video_id}_{title}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Video metadata
            f.write(f"Video: {video_info['title']}\n")
            f.write(f"URL: {video_info['url']}\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"Channel: {video_info['channel']}\n")
            f.write(f"Published: {video_info['published_at']}\n")
            f.write(f"Position in Playlist: {video_info['position'] + 1}\n")
            
            # Additional details if available
            if video_details:
                f.write(f"Duration: {self.parse_duration(video_details['duration'])}\n")
                f.write(f"View Count: {video_details['view_count']:,}\n")
                f.write(f"Like Count: {video_details['like_count']:,}\n")
                f.write(f"Comment Count: {video_details['comment_count']:,}\n")
                if video_details.get('tags'):
                    f.write(f"Tags: {', '.join(video_details['tags'][:10])}\n")  # First 10 tags
            
            # Transcript info
            f.write(f"Transcript Extracted: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Transcript Success: {transcript_data.get('success', False)}\n")
            f.write(f"Word Count: {transcript_data.get('word_count', 0)}\n")
            f.write(f"Segment Count: {transcript_data.get('segment_count', 0)}\n")
            
            if not transcript_data.get('success'):
                f.write(f"Transcript Error: {transcript_data.get('error', 'Unknown error')}\n")
            
            f.write("=" * 80 + "\n\n")
            
            # Description
            if video_info.get('description'):
                f.write("DESCRIPTION:\n")
                f.write(video_info['description'][:1000] + "...\n" if len(video_info['description']) > 1000 else video_info['description'])
                f.write("\n" + "=" * 80 + "\n\n")
            
            # Transcript
            f.write("TRANSCRIPT:\n")
            transcript = transcript_data.get("transcript", "")
            if transcript:
                f.write(transcript)
            else:
                f.write("No transcript available or extraction failed.")
        
        return filepath
    
    def process_playlist(self, playlist_url: str, languages: List[str] = ['en']) -> Dict[str, Any]:
        """Process entire playlist and extract all data."""
        print(f"🎯 YouTube Data API Playlist Extractor")
        print(f"🔗 Playlist URL: {playlist_url}")
        print(f"🌍 Languages: {languages}")
        print("=" * 80)
        
        # Extract playlist ID
        playlist_id = self.extract_playlist_id(playlist_url)
        if not playlist_id:
            print("❌ Could not extract playlist ID from URL")
            return {"error": "Invalid playlist URL"}
        
        print(f"📋 Playlist ID: {playlist_id}")
        
        # Get playlist info
        playlist_info = self.get_playlist_info(playlist_id)
        if playlist_info:
            print(f"📺 Playlist: {playlist_info['title']}")
            print(f"🎬 Channel: {playlist_info['channel']}")
            print(f"📊 Videos: {playlist_info['item_count']}")
        
        # Get playlist videos
        videos = self.get_playlist_videos(playlist_id)
        
        if not videos:
            print("❌ No videos found in playlist")
            return {"error": "No videos found", "playlist_info": playlist_info}
        
        # Get detailed video information
        video_ids = [v['video_id'] for v in videos]
        print(f"🔍 Getting detailed information for {len(video_ids)} videos...")
        video_details = self.get_video_details(video_ids)
        
        # Process each video
        extraction_results = []
        successful_transcripts = 0
        
        for i, video in enumerate(videos, 1):
            video_id = video['video_id']
            print(f"\n📹 Processing video {i}/{len(videos)}: {video['title'][:60]}...")
            
            # Get transcript
            transcript_data = self.get_transcript(video_id, languages)
            
            if transcript_data.get('success'):
                successful_transcripts += 1
                print(f"   ✅ Transcript extracted ({transcript_data['word_count']} words)")
            else:
                print(f"   ❌ Transcript failed: {transcript_data.get('error', 'Unknown error')[:50]}...")
            
            # Save video data
            filepath = self.save_video_data(
                video, 
                video_details.get(video_id, {}), 
                transcript_data, 
                i
            )
            print(f"   💾 Saved to: {filepath}")
            
            extraction_results.append({
                'video_info': video,
                'video_details': video_details.get(video_id, {}),
                'transcript_data': transcript_data,
                'filepath': filepath
            })
            
            # Be nice to the APIs
            time.sleep(0.5)
        
        # Save extraction summary
        summary_file = os.path.join(self.output_dir, "extraction_summary.json")
        summary_data = {
            'playlist_url': playlist_url,
            'playlist_id': playlist_id,
            'playlist_info': playlist_info,
            'languages': languages,
            'total_videos': len(videos),
            'successful_transcripts': successful_transcripts,
            'failed_transcripts': len(videos) - successful_transcripts,
            'extraction_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'output_directory': self.output_dir,
            'results': extraction_results
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 Extraction complete!")
        print(f"📂 Files saved to: {self.output_dir}/")
        print(f"📋 Summary: {summary_file}")
        print(f"🎬 Total videos: {len(videos)}")
        print(f"✅ Successful transcripts: {successful_transcripts}")
        print(f"❌ Failed transcripts: {len(videos) - successful_transcripts}")
        
        return summary_data


def main():
    """Main function to run the YouTube Data API extractor."""
    
    # Get API key from environment or command line
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    # If no API key in environment, check command line arguments
    if not api_key or api_key.startswith('your-'):
        if len(sys.argv) > 1:
            api_key = sys.argv[1]
        else:
            print("❌ YouTube API Key needed!")
            print("   Option 1: Set environment variable:")
            print("   export YOUTUBE_API_KEY='your_actual_api_key_here'")
            print("   Option 2: Pass as command line argument:")
            print("   python youtube_data_api_extractor.py YOUR_API_KEY")
            print()
            print("   Get your YouTube Data API v3 key from:")
            print("   https://console.cloud.google.com/apis/credentials")
            return
    
    # Your playlist URL
    playlist_url = "https://www.youtube.com/playlist?list=PLhRDeFiayugWdr3hCkNeVFhWXS0oTuJZK"
    
    print("🚀 YouTube Data API Playlist Extractor")
    print("=" * 50)
    print(f"🔑 Using API key: {api_key[:10]}...")
    
    # Create extractor and run
    extractor = YouTubeDataAPIExtractor(api_key)
    results = extractor.process_playlist(playlist_url)
    
    # Print final summary
    if 'error' not in results:
        print(f"\n🎯 Final Summary:")
        print(f"   📋 Total videos: {results.get('total_videos', 0)}")
        print(f"   ✅ Successful transcripts: {results.get('successful_transcripts', 0)}")
        print(f"   ❌ Failed transcripts: {results.get('failed_transcripts', 0)}")
        print(f"   📂 Output directory: {results.get('output_directory', 'N/A')}")
        
        if results.get('successful_transcripts', 0) > 0:
            print(f"\n🎉 Success! Real YouTube playlist data extracted!")
            print(f"💡 Check the output directory for complete video data and transcripts.")
        else:
            print(f"\n⚠️  No transcripts were extracted, but video metadata is available.")
    else:
        print(f"\n❌ Error: {results.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main() 