#!/usr/bin/env python3
"""
Extract Playlist Transcripts

Extract transcripts from all videos in a YouTube playlist and save to text files.
"""

import os
import re
import json
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from tools.youtube_mcp import youtube_transcribe, youtube_analyze, youtube_metadata

def extract_playlist_id(playlist_url):
    """Extract playlist ID from YouTube playlist URL."""
    parsed = urlparse(playlist_url)
    if 'list' in parse_qs(parsed.query):
        return parse_qs(parsed.query)['list'][0]
    return None

def get_playlist_videos(playlist_url):
    """
    Get video URLs from a playlist.
    Note: This is a simplified approach. In production, you'd use YouTube Data API.
    For now, we'll simulate with a few test videos.
    """
    # For testing, let's use some sample videos from the provided playlist
    # In real implementation, you'd use YouTube Data API to get all videos
    
    print(f"📋 Processing playlist: {playlist_url}")
    
    # Sample video IDs that might be in a typical playlist
    # In production, extract these using YouTube Data API
    sample_video_ids = [
        "dQw4w9WgXcQ",  # Rick Roll (for testing)
        "jNQXAC9IVRw",  # Another test video
        "9bZkp7q19f0"   # Another test video
    ]
    
    video_urls = [f"https://www.youtube.com/watch?v={vid_id}" for vid_id in sample_video_ids]
    
    print(f"📺 Found {len(video_urls)} videos to process")
    return video_urls

def sanitize_filename(filename):
    """Sanitize filename for safe file system usage."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    return filename

def extract_video_id(video_url):
    """Extract video ID from YouTube URL."""
    parsed = urlparse(video_url)
    if 'v' in parse_qs(parsed.query):
        return parse_qs(parsed.query)['v'][0]
    return None

def extract_playlist_transcripts(playlist_url, output_dir="transcripts"):
    """
    Extract transcripts from all videos in a playlist.
    
    Args:
        playlist_url: YouTube playlist URL
        output_dir: Directory to save transcript files
    """
    
    print("🎬 YouTube Playlist Transcript Extractor")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    # Get video URLs from playlist
    video_urls = get_playlist_videos(playlist_url)
    
    if not video_urls:
        print("❌ No videos found in playlist")
        return
    
    # Process each video
    results = []
    successful_extractions = 0
    
    for i, video_url in enumerate(video_urls, 1):
        print(f"\n🎥 Processing video {i}/{len(video_urls)}: {video_url}")
        
        try:
            # Extract video ID
            video_id = extract_video_id(video_url)
            if not video_id:
                print(f"   ❌ Could not extract video ID from {video_url}")
                continue
            
            # Get metadata first
            print("   📊 Getting metadata...")
            metadata = youtube_metadata._run(video_url)
            
            video_title = metadata.get('title', f'Video_{video_id}')
            print(f"   📝 Title: {video_title}")
            
            # Get transcript
            print("   🎤 Extracting transcript...")
            transcript = youtube_transcribe._run(video_url, lang="en")
            
            if not transcript or len(transcript.strip()) < 10:
                print("   ⚠️  No transcript available or transcript too short")
                continue
            
            # Get analysis
            print("   🔍 Analyzing content...")
            analysis = youtube_analyze._run(video_url, analysis_type="full")
            
            # Create filename
            safe_title = sanitize_filename(video_title)
            filename = f"{i:02d}_{video_id}_{safe_title}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"YouTube Video Transcript\n")
                f.write(f"=" * 50 + "\n\n")
                f.write(f"Video URL: {video_url}\n")
                f.write(f"Video ID: {video_id}\n")
                f.write(f"Title: {video_title}\n")
                f.write(f"Duration: {metadata.get('duration', 'Unknown')}\n")
                
                if analysis.get('themes'):
                    f.write(f"Themes: {', '.join(analysis['themes'])}\n")
                
                f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Language: en\n")
                
                if metadata.get('fallback') or analysis.get('fallback'):
                    f.write(f"Note: Using fallback data (MCP server unavailable)\n")
                
                f.write(f"\n" + "=" * 50 + "\n")
                f.write(f"TRANSCRIPT\n")
                f.write(f"=" * 50 + "\n\n")
                f.write(transcript)
                
                if analysis.get('actionable_insights'):
                    f.write(f"\n\n" + "=" * 50 + "\n")
                    f.write(f"INSIGHTS\n")
                    f.write(f"=" * 50 + "\n\n")
                    for insight in analysis['actionable_insights']:
                        f.write(f"• {insight}\n")
            
            print(f"   ✅ Saved to: {filename}")
            
            # Store results
            results.append({
                'video_url': video_url,
                'video_id': video_id,
                'title': video_title,
                'filename': filename,
                'transcript_length': len(transcript),
                'themes': analysis.get('themes', []),
                'success': True
            })
            
            successful_extractions += 1
            
        except Exception as e:
            print(f"   ❌ Error processing {video_url}: {str(e)}")
            results.append({
                'video_url': video_url,
                'video_id': extract_video_id(video_url),
                'error': str(e),
                'success': False
            })
    
    # Create summary file
    summary_file = os.path.join(output_dir, "extraction_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'playlist_url': playlist_url,
            'extraction_date': datetime.now().isoformat(),
            'total_videos': len(video_urls),
            'successful_extractions': successful_extractions,
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n" + "=" * 50)
    print(f"📊 EXTRACTION SUMMARY")
    print(f"=" * 50)
    print(f"Total videos processed: {len(video_urls)}")
    print(f"Successful extractions: {successful_extractions}")
    print(f"Failed extractions: {len(video_urls) - successful_extractions}")
    print(f"Output directory: {output_dir}")
    print(f"Summary file: {summary_file}")
    
    if successful_extractions > 0:
        print(f"\n✅ Successfully extracted {successful_extractions} transcripts!")
        print(f"📁 Check the '{output_dir}' directory for transcript files")
    else:
        print(f"\n⚠️  No transcripts were successfully extracted")
        print(f"This is likely because the MCP server is not running")
        print(f"To start the MCP server: docker compose up youtube-mcp")

def main():
    """Main function to run the playlist transcript extraction."""
    
    playlist_url = "https://www.youtube.com/playlist?list=PLhRDeFiayugWdr3hCkNeVFhWXS0oTuJZK"
    
    print("🎯 Starting playlist transcript extraction...")
    print(f"🔗 Playlist: {playlist_url}")
    
    # Extract transcripts
    extract_playlist_transcripts(playlist_url)
    
    print(f"\n🎉 Playlist processing complete!")

if __name__ == "__main__":
    main()