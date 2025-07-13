#!/usr/bin/env python3
"""
Single Video Extractor

Test script to extract data from a single YouTube video using YouTube Data API v3.
"""

import os
import json
import time
import re
import sys
from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class SingleVideoExtractor:
    def __init__(self, api_key: str, output_dir: str = "single_video_output"):
        """Initialize the single video extractor."""
        self.api_key = api_key
        self.output_dir = output_dir
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.ensure_output_dir()
        
    def ensure_output_dir(self):
        """Ensure the output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def extract_video_id(self, video_url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
            r'youtube\.com/v/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, video_url)
            if match:
                return match.group(1)
        return None
    
    def get_video_details(self, video_id: str) -> Dict[str, Any]:
        """Get detailed video information from YouTube Data API."""
        try:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                video = response['items'][0]
                snippet = video['snippet']
                content_details = video['contentDetails']
                stats = video['statistics']
                
                return {
                    'video_id': video_id,
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'channel': snippet['channelTitle'],
                    'channel_id': snippet['channelId'],
                    'published_at': snippet['publishedAt'],
                    'duration': content_details['duration'],
                    'view_count': int(stats.get('viewCount', 0)),
                    'like_count': int(stats.get('likeCount', 0)),
                    'comment_count': int(stats.get('commentCount', 0)),
                    'tags': snippet.get('tags', []),
                    'category_id': snippet['categoryId'],
                    'default_language': snippet.get('defaultLanguage', 'en'),
                    'thumbnail': snippet['thumbnails']['high']['url'] if 'high' in snippet['thumbnails'] else snippet['thumbnails']['default']['url'],
                    'success': True
                }
            else:
                return {'success': False, 'error': 'Video not found'}
                
        except HttpError as e:
            return {'success': False, 'error': f'API Error: {e}'}
        except Exception as e:
            return {'success': False, 'error': f'Unexpected error: {e}'}
    
    def parse_duration(self, duration_str: str) -> str:
        """Parse ISO 8601 duration to readable format."""
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
    
    def get_transcript(self, video_id: str, languages: list = ['en']) -> Dict[str, Any]:
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
    
    def format_transcript(self, transcript_list: list) -> str:
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
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\s+', ' ', filename)
        return filename.strip()[:150]  # Limit length
    
    def save_video_data(self, video_details: Dict[str, Any], transcript_data: Dict[str, Any]) -> str:
        """Save video data and transcript to a text file."""
        if not video_details.get('success'):
            print(f"❌ Cannot save video data: {video_details.get('error', 'Unknown error')}")
            return ""
            
        video_id = video_details['video_id']
        title = self.sanitize_filename(video_details['title'])
        
        filename = f"{video_id}_{title}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Video metadata
            f.write(f"Video: {video_details['title']}\n")
            f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
            f.write(f"Video ID: {video_id}\n")
            f.write(f"Channel: {video_details['channel']}\n")
            f.write(f"Channel ID: {video_details['channel_id']}\n")
            f.write(f"Published: {video_details['published_at']}\n")
            f.write(f"Duration: {self.parse_duration(video_details['duration'])}\n")
            f.write(f"View Count: {video_details['view_count']:,}\n")
            f.write(f"Like Count: {video_details['like_count']:,}\n")
            f.write(f"Comment Count: {video_details['comment_count']:,}\n")
            
            if video_details.get('tags'):
                f.write(f"Tags: {', '.join(video_details['tags'][:15])}\n")
            
            # Transcript info
            f.write(f"Transcript Extracted: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Transcript Success: {transcript_data.get('success', False)}\n")
            f.write(f"Word Count: {transcript_data.get('word_count', 0)}\n")
            f.write(f"Segment Count: {transcript_data.get('segment_count', 0)}\n")
            
            if not transcript_data.get('success'):
                f.write(f"Transcript Error: {transcript_data.get('error', 'Unknown error')}\n")
            
            f.write("=" * 80 + "\n\n")
            
            # Description
            if video_details.get('description'):
                f.write("DESCRIPTION:\n")
                desc = video_details['description']
                f.write(desc[:2000] + "...\n" if len(desc) > 2000 else desc + "\n")
                f.write("\n" + "=" * 80 + "\n\n")
            
            # Transcript
            f.write("TRANSCRIPT:\n")
            transcript = transcript_data.get("transcript", "")
            if transcript:
                f.write(transcript)
            else:
                f.write("No transcript available or extraction failed.")
        
        return filepath
    
    def process_video(self, video_url: str) -> Dict[str, Any]:
        """Process a single video and extract all data."""
        print(f"🎯 Single Video Extractor")
        print(f"🔗 Video URL: {video_url}")
        print("=" * 60)
        
        # Extract video ID
        video_id = self.extract_video_id(video_url)
        if not video_id:
            print("❌ Could not extract video ID from URL")
            return {"error": "Invalid video URL"}
        
        print(f"📺 Video ID: {video_id}")
        
        # Get video details
        print(f"🔍 Getting video details from YouTube Data API...")
        video_details = self.get_video_details(video_id)
        
        if not video_details.get('success'):
            print(f"❌ Failed to get video details: {video_details.get('error')}")
            return video_details
        
        print(f"✅ Video: {video_details['title']}")
        print(f"🎬 Channel: {video_details['channel']}")
        print(f"⏱️  Duration: {self.parse_duration(video_details['duration'])}")
        print(f"👀 Views: {video_details['view_count']:,}")
        
        # Get transcript
        print(f"📝 Attempting to extract transcript...")
        transcript_data = self.get_transcript(video_id)
        
        if transcript_data.get('success'):
            print(f"✅ Transcript extracted ({transcript_data['word_count']} words)")
        else:
            print(f"❌ Transcript failed: {transcript_data.get('error', 'Unknown error')}")
        
        # Save data
        print(f"💾 Saving video data...")
        filepath = self.save_video_data(video_details, transcript_data)
        
        if filepath:
            print(f"✅ Saved to: {filepath}")
        
        # Create summary
        summary_data = {
            'video_url': video_url,
            'video_id': video_id,
            'video_details': video_details,
            'transcript_data': transcript_data,
            'filepath': filepath,
            'extraction_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'output_directory': self.output_dir
        }
        
        # Save JSON summary
        summary_file = os.path.join(self.output_dir, f"{video_id}_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Summary saved to: {summary_file}")
        print(f"\n🎉 Video extraction complete!")
        
        return summary_data


def main():
    """Main function to run the single video extractor."""
    
    # Get API key from environment or command line
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key or api_key.startswith('your-'):
        if len(sys.argv) > 2:
            api_key = sys.argv[1]
            video_url = sys.argv[2]
        elif len(sys.argv) > 1:
            print("❌ Need both API key and video URL!")
            print("   Usage: python single_video_extractor.py API_KEY VIDEO_URL")
            print("   Or set YOUTUBE_API_KEY and provide just the video URL:")
            print("   python single_video_extractor.py VIDEO_URL")
            return
        else:
            print("❌ YouTube API Key and Video URL needed!")
            print("   Usage: python single_video_extractor.py API_KEY VIDEO_URL")
            print("   Or set: export YOUTUBE_API_KEY='your_key'")
            print("         python single_video_extractor.py VIDEO_URL")
            return
    else:
        if len(sys.argv) > 1:
            video_url = sys.argv[1]
        else:
            # Default video for testing
            video_url = "https://youtu.be/DVGSXt4C8z0?si=dQqVr5KbErz2yGaG"
    
    print("🚀 Single Video YouTube Data Extractor")
    print("=" * 40)
    print(f"🔑 Using API key: {api_key[:10]}...")
    
    # Create extractor and run
    extractor = SingleVideoExtractor(api_key)
    results = extractor.process_video(video_url)
    
    # Print final summary
    if 'error' not in results:
        print(f"\n🎯 Final Summary:")
        print(f"   📺 Video: {results['video_details']['title'][:50]}...")
        print(f"   ⏱️  Duration: {extractor.parse_duration(results['video_details']['duration'])}")
        print(f"   👀 Views: {results['video_details']['view_count']:,}")
        print(f"   📝 Transcript: {'✅ Success' if results['transcript_data']['success'] else '❌ Failed'}")
        print(f"   📂 Output: {results['output_directory']}")
        
        if results['transcript_data']['success']:
            print(f"\n🎉 Success! Video data and transcript extracted!")
        else:
            print(f"\n⚠️  Video metadata extracted, but transcript failed.")
            print(f"💡 Transcript error: {results['transcript_data'].get('error', 'Unknown')}")
    else:
        print(f"\n❌ Error: {results.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main() 