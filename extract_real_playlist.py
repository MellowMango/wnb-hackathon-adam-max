#!/usr/bin/env python3
"""
Real Playlist Transcript Extractor

Extract transcripts from a real YouTube playlist using the YouTube Data API
and the integrated MCP server.
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

def get_playlist_videos_api(playlist_id, max_results=50):
    """
    Get video URLs from a playlist using YouTube Data API.
    
    Args:
        playlist_id: YouTube playlist ID
        max_results: Maximum number of videos to retrieve
    """
    api_key = os.getenv("YOUTUBE_API_KEY")
    
    if not api_key:
        print("⚠️  No YOUTUBE_API_KEY found in environment")
        print("   Using sample videos for demonstration")
        return get_sample_videos()
    
    try:
        url = "https://www.googleapis.com/youtube/v3/playlistItems"
        params = {
            'part': 'snippet',
            'playlistId': playlist_id,
            'maxResults': max_results,
            'key': api_key
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        videos = []
        for item in data.get('items', []):
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            videos.append({
                'url': video_url,
                'id': video_id,
                'title': title,
                'published': item['snippet']['publishedAt']
            })
        
        print(f"📺 Found {len(videos)} videos in playlist via YouTube API")
        return videos
        
    except Exception as e:
        print(f"❌ Error fetching playlist via API: {e}")
        print("   Using sample videos for demonstration")
        return get_sample_videos()

def get_sample_videos():
    """Get sample videos for testing when API is not available."""
    return [
        {
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'id': 'dQw4w9WgXcQ', 
            'title': 'Rick Astley - Never Gonna Give You Up',
            'published': '2009-10-25T06:57:33Z'
        },
        {
            'url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw',
            'id': 'jNQXAC9IVRw',
            'title': 'Me at the zoo',
            'published': '2005-04-23T23:35:47Z'
        }
    ]

def check_mcp_server():
    """Check if the YouTube MCP server is running."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        response.raise_for_status()
        print("✅ YouTube MCP server is running")
        return True
    except Exception as e:
        print("❌ YouTube MCP server is not running")
        print(f"   Error: {e}")
        print(f"   To start: docker compose up youtube-mcp")
        return False

def sanitize_filename(filename):
    """Sanitize filename for safe file system usage."""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.replace('\n', ' ').replace('\r', '')
    if len(filename) > 100:
        filename = filename[:100]
    return filename.strip()

def extract_playlist_transcripts(playlist_url, output_dir="playlist_transcripts"):
    """
    Extract transcripts from all videos in a playlist.
    
    Args:
        playlist_url: YouTube playlist URL
        output_dir: Directory to save transcript files
    """
    
    print("🎬 Real YouTube Playlist Transcript Extractor")
    print("=" * 60)
    print(f"🔗 Playlist: {playlist_url}")
    
    # Check MCP server status
    mcp_available = check_mcp_server()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    # Extract playlist ID
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print("❌ Could not extract playlist ID from URL")
        return
    
    print(f"📋 Playlist ID: {playlist_id}")
    
    # Get video URLs from playlist
    videos = get_playlist_videos_api(playlist_id)
    
    if not videos:
        print("❌ No videos found in playlist")
        return
    
    # Process each video
    results = []
    successful_extractions = 0
    
    for i, video_info in enumerate(videos, 1):
        video_url = video_info['url']
        video_id = video_info['id']
        expected_title = video_info['title']
        
        print(f"\n🎥 Processing video {i}/{len(videos)}")
        print(f"   📺 {expected_title}")
        print(f"   🔗 {video_url}")
        
        try:
            # Get metadata
            print("   📊 Getting metadata...")
            metadata = youtube_metadata._run(video_url)
            
            video_title = metadata.get('title', expected_title)
            is_fallback = metadata.get('fallback', False)
            
            # Get transcript
            print("   🎤 Extracting transcript...")
            transcript = youtube_transcribe._run(video_url, lang="en")
            
            if not transcript or len(transcript.strip()) < 10:
                print("   ⚠️  No transcript available or transcript too short")
                if not mcp_available:
                    print("      (MCP server not running - this is expected)")
            
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
                f.write(f"=" * 60 + "\n\n")
                f.write(f"Video URL: {video_url}\n")
                f.write(f"Video ID: {video_id}\n")
                f.write(f"Title: {video_title}\n")
                f.write(f"Expected Title: {expected_title}\n")
                f.write(f"Duration: {metadata.get('duration', 'Unknown')}\n")
                f.write(f"Published: {video_info.get('published', 'Unknown')}\n")
                
                if analysis.get('themes'):
                    f.write(f"Themes: {', '.join(analysis['themes'])}\n")
                
                f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Language: en\n")
                
                if is_fallback or analysis.get('fallback'):
                    f.write(f"Note: Using fallback data (MCP server unavailable)\n")
                    if not mcp_available:
                        f.write(f"      To get real transcripts: docker compose up youtube-mcp\n")
                
                f.write(f"\n" + "=" * 60 + "\n")
                f.write(f"TRANSCRIPT\n")
                f.write(f"=" * 60 + "\n\n")
                
                if transcript.startswith("Error"):
                    f.write(f"[TRANSCRIPT EXTRACTION ERROR]\n")
                    f.write(f"{transcript}\n\n")
                    f.write(f"To get real transcripts:\n")
                    f.write(f"1. Start the MCP server: docker compose up youtube-mcp\n")
                    f.write(f"2. Re-run this script\n")
                else:
                    f.write(transcript)
                
                if analysis.get('actionable_insights'):
                    f.write(f"\n\n" + "=" * 60 + "\n")
                    f.write(f"INSIGHTS\n")
                    f.write(f"=" * 60 + "\n\n")
                    for insight in analysis['actionable_insights']:
                        f.write(f"• {insight}\n")
                
                # Add raw analysis data
                f.write(f"\n\n" + "=" * 60 + "\n")
                f.write(f"RAW ANALYSIS DATA\n")
                f.write(f"=" * 60 + "\n\n")
                f.write(json.dumps(analysis, indent=2, ensure_ascii=False))
            
            print(f"   ✅ Saved to: {filename}")
            
            # Store results
            results.append({
                'video_url': video_url,
                'video_id': video_id,
                'title': video_title,
                'expected_title': expected_title,
                'filename': filename,
                'transcript_length': len(transcript),
                'themes': analysis.get('themes', []),
                'success': True,
                'fallback_used': is_fallback or analysis.get('fallback', False)
            })
            
            successful_extractions += 1
            
        except Exception as e:
            print(f"   ❌ Error processing {video_url}: {str(e)}")
            results.append({
                'video_url': video_url,
                'video_id': video_id,
                'expected_title': expected_title,
                'error': str(e),
                'success': False
            })
    
    # Create summary file
    summary_file = os.path.join(output_dir, "playlist_extraction_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'playlist_url': playlist_url,
            'playlist_id': playlist_id,
            'extraction_date': datetime.now().isoformat(),
            'mcp_server_available': mcp_available,
            'total_videos': len(videos),
            'successful_extractions': successful_extractions,
            'youtube_api_used': bool(os.getenv("YOUTUBE_API_KEY")),
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    # Create index file
    index_file = os.path.join(output_dir, "README.md")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(f"# Playlist Transcript Extraction Results\n\n")
        f.write(f"**Playlist:** {playlist_url}\n")
        f.write(f"**Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Videos:** {len(videos)}\n")
        f.write(f"**Successful Extractions:** {successful_extractions}\n")
        f.write(f"**MCP Server Available:** {'✅ Yes' if mcp_available else '❌ No'}\n\n")
        
        if not mcp_available:
            f.write(f"⚠️ **Note:** Real transcripts require the MCP server to be running.\n")
            f.write(f"To start: `docker compose up youtube-mcp`\n\n")
        
        f.write(f"## Files\n\n")
        for i, result in enumerate(results, 1):
            if result['success']:
                status = "✅" if not result.get('fallback_used') else "⚠️"
                f.write(f"{i}. {status} [{result['filename']}](./{result['filename']})\n")
                f.write(f"   - **Title:** {result['title']}\n")
                f.write(f"   - **Video ID:** {result['video_id']}\n")
                f.write(f"   - **Transcript Length:** {result['transcript_length']} chars\n")
                if result.get('themes'):
                    f.write(f"   - **Themes:** {', '.join(result['themes'])}\n")
                f.write(f"\n")
            else:
                f.write(f"{i}. ❌ Failed: {result['expected_title']}\n")
                f.write(f"   - **Error:** {result['error']}\n\n")
    
    # Print summary
    print(f"\n" + "=" * 60)
    print(f"📊 EXTRACTION SUMMARY")
    print(f"=" * 60)
    print(f"Playlist: {playlist_url}")
    print(f"Total videos processed: {len(videos)}")
    print(f"Successful extractions: {successful_extractions}")
    print(f"Failed extractions: {len(videos) - successful_extractions}")
    print(f"MCP server available: {'✅ Yes' if mcp_available else '❌ No'}")
    print(f"Output directory: {output_dir}")
    print(f"Summary file: {summary_file}")
    print(f"Index file: {index_file}")
    
    if successful_extractions > 0:
        print(f"\n✅ Successfully processed {successful_extractions} videos!")
        print(f"📁 Check the '{output_dir}' directory for transcript files")
        if not mcp_available:
            print(f"⚠️  Using fallback data. For real transcripts:")
            print(f"   1. Start MCP server: docker compose up youtube-mcp")
            print(f"   2. Re-run this script")
    else:
        print(f"\n❌ No transcripts were successfully extracted")

def main():
    """Main function to run the playlist transcript extraction."""
    
    playlist_url = "https://www.youtube.com/playlist?list=PLhRDeFiayugWdr3hCkNeVFhWXS0oTuJZK"
    
    print("🎯 Starting real playlist transcript extraction...")
    print(f"🔗 Target playlist: {playlist_url}")
    
    # Check environment
    if os.getenv("YOUTUBE_API_KEY"):
        print("✅ YouTube API key found - will fetch real playlist data")
    else:
        print("⚠️  No YouTube API key - will use sample videos")
        print("   Set YOUTUBE_API_KEY environment variable for real playlist data")
    
    # Extract transcripts
    extract_playlist_transcripts(playlist_url)
    
    print(f"\n🎉 Playlist processing complete!")
    print(f"💡 Next steps:")
    print(f"   1. Review transcripts in the output directory")
    print(f"   2. Use them for CrewAI content analysis")
    print(f"   3. Generate local experience recommendations")

if __name__ == "__main__":
    main()