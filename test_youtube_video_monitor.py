#!/usr/bin/env python3
"""
YouTube Video Monitor Test Suite

This script tests the new video-focused YouTube monitor functionality.
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add youtube_monitor to path
youtube_monitor_path = str(Path(__file__).parent / "youtube_monitor" / "src")
sys.path.insert(0, youtube_monitor_path)

def test_video_id_extraction():
    """Test video ID extraction from various URL formats."""
    print("🔧 Testing Video ID Extraction...")
    
    try:
        from monitor import extract_video_id
        
        # Test cases: (input, expected_output)
        test_cases = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/v/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30", "dQw4w9WgXcQ"),
            ("invalid_url", None),
            ("", None),
        ]
        
        for input_url, expected in test_cases:
            result = extract_video_id(input_url)
            if result == expected:
                print(f"✅ {input_url} -> {result}")
            else:
                print(f"❌ {input_url} -> {result} (expected {expected})")
                return False
        
        print("✅ Video ID extraction test passed")
        return True
        
    except Exception as e:
        print(f"❌ Video ID extraction test failed: {e}")
        return False

def test_video_monitor_initialization():
    """Test YouTubeVideoMonitor initialization."""
    print("\n🤖 Testing Video Monitor Initialization...")
    
    try:
        from monitor import YouTubeVideoMonitor
        
        # Mock the YouTube API client
        with patch('monitor.build') as mock_build:
            mock_youtube = Mock()
            mock_build.return_value = mock_youtube
            
            # Test with temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                monitor = YouTubeVideoMonitor(
                    api_key="test_api_key",
                    output_dir=temp_dir
                )
                
                # Check initialization
                assert monitor.api_key == "test_api_key"
                assert str(monitor.output_dir) == temp_dir
                
                print("✅ Video monitor initialization successful")
                print(f"✅ API key: {monitor.api_key}")
                print(f"✅ Output directory: {monitor.output_dir}")
                
                return True
        
    except Exception as e:
        print(f"❌ Video monitor initialization test failed: {e}")
        return False

def test_video_metadata_extraction():
    """Test video metadata extraction."""
    print("\n📹 Testing Video Metadata Extraction...")
    
    try:
        from monitor import YouTubeVideoMonitor
        
        with patch('monitor.build') as mock_build:
            mock_youtube = Mock()
            mock_build.return_value = mock_youtube
            
            # Mock the API response
            mock_response = {
                'items': [{
                    'id': 'test_video_id',
                    'snippet': {
                        'title': 'Test Video Title',
                        'description': 'Test video description',
                        'publishedAt': '2024-01-01T00:00:00Z',
                        'channelTitle': 'Test Channel',
                        'channelId': 'test_channel_id',
                        'tags': ['test', 'video'],
                        'categoryId': '22',
                        'defaultLanguage': 'en'
                    },
                    'statistics': {
                        'viewCount': '1000',
                        'likeCount': '100',
                        'commentCount': '10'
                    },
                    'contentDetails': {
                        'duration': 'PT10M30S',
                        'definition': 'hd',
                        'caption': 'true',
                        'licensedContent': False,
                        'projection': 'rectangular'
                    }
                }]
            }
            
            mock_youtube.videos.return_value.list.return_value.execute.return_value = mock_response
            
            with tempfile.TemporaryDirectory() as temp_dir:
                monitor = YouTubeVideoMonitor(
                    api_key="test_api_key",
                    output_dir=temp_dir
                )
                
                # Test metadata extraction
                metadata = monitor.get_video_metadata("test_video_id")
                
                assert metadata['title'] == 'Test Video Title'
                assert metadata['view_count'] == '1000'
                assert metadata['duration'] == 'PT10M30S'
                
                print("✅ Video metadata extraction successful")
                print(f"✅ Title: {metadata['title']}")
                print(f"✅ Views: {metadata['view_count']}")
                print(f"✅ Duration: {metadata['duration']}")
                
                return True
        
    except Exception as e:
        print(f"❌ Video metadata extraction test failed: {e}")
        return False

def test_video_processing():
    """Test complete video processing workflow."""
    print("\n⚙️ Testing Video Processing Workflow...")
    
    try:
        from monitor import YouTubeVideoMonitor
        
        with patch('monitor.build') as mock_build:
            mock_youtube = Mock()
            mock_build.return_value = mock_youtube
            
            # Mock the API response
            mock_response = {
                'items': [{
                    'id': 'dQw4w9WgXcQ',
                    'snippet': {
                        'title': 'Rick Astley - Never Gonna Give You Up',
                        'description': 'Official music video',
                        'publishedAt': '2009-10-25T06:57:33Z',
                        'channelTitle': 'Rick Astley',
                        'channelId': 'UCuAXFkgsw1L7xaCfnd5JJOw',
                        'tags': ['rick', 'astley'],
                        'categoryId': '10',
                        'defaultLanguage': 'en'
                    },
                    'statistics': {
                        'viewCount': '1000000000',
                        'likeCount': '10000000',
                        'commentCount': '1000000'
                    },
                    'contentDetails': {
                        'duration': 'PT3M33S',
                        'definition': 'hd',
                        'caption': 'true',
                        'licensedContent': False,
                        'projection': 'rectangular'
                    }
                }]
            }
            
            mock_youtube.videos.return_value.list.return_value.execute.return_value = mock_response
            
            with tempfile.TemporaryDirectory() as temp_dir:
                monitor = YouTubeVideoMonitor(
                    api_key="test_api_key",
                    output_dir=temp_dir
                )
                
                # Mock transcript extraction
                with patch('monitor.YouTubeTranscriptApi') as mock_transcript:
                    mock_transcript.get_transcript.return_value = [
                        {'text': 'Never gonna give you up', 'start': 0.0, 'duration': 2.0},
                        {'text': 'Never gonna let you down', 'start': 2.0, 'duration': 3.0}
                    ]
                    
                    # Test video processing
                    video_dir = monitor.process_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                    
                    assert video_dir is not None
                    assert video_dir.exists()
                    
                    # Check if files were created
                    metadata_file = video_dir / "metadata.json"
                    transcript_file = video_dir / "transcript.txt"
                    summary_file = video_dir / "summary.txt"
                    
                    assert metadata_file.exists()
                    assert transcript_file.exists()
                    assert summary_file.exists()
                    
                    print("✅ Video processing workflow successful")
                    print(f"✅ Output directory: {video_dir}")
                    print(f"✅ Files created: {len(list(video_dir.glob('*')))} files")
                    
                    # Test metadata content
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                        assert metadata['title'] == 'Rick Astley - Never Gonna Give You Up'
                        print(f"✅ Metadata saved correctly: {metadata['title']}")
                    
                    return True
        
    except Exception as e:
        print(f"❌ Video processing test failed: {e}")
        return False

def test_cli_interface():
    """Test CLI interface with video URL."""
    print("\n💬 Testing CLI Interface...")
    
    try:
        from cli import extract_video_id
        
        # Test that CLI can extract video ID (basic test)
        video_id = extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert video_id == "dQw4w9WgXcQ"
        
        print("✅ CLI interface test passed")
        return True
        
    except Exception as e:
        print(f"❌ CLI interface test failed: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    print("🎬 YouTube Video Monitor Test Suite")
    print("=" * 50)
    
    tests = [
        test_video_id_extraction,
        test_video_monitor_initialization,
        test_video_metadata_extraction,
        test_video_processing,
        test_cli_interface,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print(f"\n📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! The video monitor is working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 