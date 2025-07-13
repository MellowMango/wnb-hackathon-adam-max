#!/usr/bin/env python3
"""
YouTube Monitor Script Test Suite

This script comprehensively tests the YouTube monitor script functionality.
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add youtube_monitor to path
youtube_monitor_path = str(Path(__file__).parent / "youtube_monitor" / "src")
config_path = str(Path(__file__).parent / "youtube_monitor")
sys.path.insert(0, youtube_monitor_path)
sys.path.insert(0, config_path)

def test_imports():
    """Test that all required modules can be imported."""
    print("🔧 Testing Imports...")
    
    try:
        # Test core module imports
        from monitor import YouTubePlaylistMonitor
        print("✅ monitor.py import successful")
        
        # Test CLI module
        from cli import main as cli_main
        print("✅ cli.py import successful")
        
        # Test config module
        from config.settings import Settings
        print("✅ config.settings import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_settings_configuration():
    """Test settings and configuration."""
    print("\n⚙️  Testing Configuration...")
    
    try:
        from config.settings import Settings
        
        # Test settings initialization
        settings = Settings()
        print("✅ Settings initialization successful")
        
        # Test settings validation with empty values
        settings.youtube_api_key = ""
        settings.playlist_id = ""
        if not settings.validate():
            print("✅ Settings validation correctly rejects empty values")
        else:
            print("❌ Settings validation should reject empty values")
            return False
        
        # Test settings validation with valid values
        settings.youtube_api_key = "test_key"
        settings.playlist_id = "test_playlist"
        if settings.validate():
            print("✅ Settings validation correctly accepts valid values")
        else:
            print("❌ Settings validation should accept valid values")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_monitor_initialization():
    """Test monitor initialization."""
    print("\n🤖 Testing Monitor Initialization...")
    
    try:
        from monitor import YouTubePlaylistMonitor
        
        # Mock the YouTube API client
        with patch('monitor.build') as mock_build:
            mock_youtube = Mock()
            mock_build.return_value = mock_youtube
            
            # Test with temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                monitor = YouTubePlaylistMonitor(
                    api_key="test_api_key",
                    playlist_id="test_playlist_id",
                    output_dir=temp_dir
                )
                
                # Check initialization
                assert monitor.api_key == "test_api_key"
                assert monitor.playlist_id == "test_playlist_id"
                assert str(monitor.output_dir) == temp_dir
                
                print("✅ Monitor initialization successful")
                print(f"✅ API key: {monitor.api_key}")
                print(f"✅ Playlist ID: {monitor.playlist_id}")
                print(f"✅ Output directory: {monitor.output_dir}")
                
                return True
        
    except Exception as e:
        print(f"❌ Monitor initialization test failed: {e}")
        return False

def test_processed_videos_tracking():
    """Test processed videos tracking."""
    print("\n📊 Testing Processed Videos Tracking...")
    
    try:
        from monitor import YouTubePlaylistMonitor
        
        with patch('monitor.build') as mock_build:
            mock_youtube = Mock()
            mock_build.return_value = mock_youtube
            
            with tempfile.TemporaryDirectory() as temp_dir:
                monitor = YouTubePlaylistMonitor(
                    api_key="test_api_key",
                    playlist_id="test_playlist_id",
                    output_dir=temp_dir
                )
                
                # Test initial state
                assert len(monitor.processed_videos) == 0
                print("✅ Initial processed videos list is empty")
                
                # Test adding processed video
                monitor.processed_videos.add("test_video_id")
                assert "test_video_id" in monitor.processed_videos
                print("✅ Video successfully added to processed list")
                
                # Test saving and loading
                monitor._save_processed_videos()
                
                # Create new monitor instance to test loading
                monitor2 = YouTubePlaylistMonitor(
                    api_key="test_api_key",
                    playlist_id="test_playlist_id",
                    output_dir=temp_dir
                )
                
                assert "test_video_id" in monitor2.processed_videos
                print("✅ Processed videos persistence works correctly")
                
                return True
        
    except Exception as e:
        print(f"❌ Processed videos tracking test failed: {e}")
        return False

def test_video_metadata_extraction():
    """Test video metadata extraction functionality."""
    print("\n📹 Testing Video Metadata Extraction...")
    
    try:
        from monitor import YouTubePlaylistMonitor
        
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
                monitor = YouTubePlaylistMonitor(
                    api_key="test_api_key",
                    playlist_id="test_playlist_id",
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

def test_transcript_extraction():
    """Test video transcript extraction."""
    print("\n📝 Testing Transcript Extraction...")
    
    try:
        from monitor import YouTubePlaylistMonitor
        
        with patch('monitor.build') as mock_build:
            mock_youtube = Mock()
            mock_build.return_value = mock_youtube
            
            with tempfile.TemporaryDirectory() as temp_dir:
                monitor = YouTubePlaylistMonitor(
                    api_key="test_api_key",
                    playlist_id="test_playlist_id",
                    output_dir=temp_dir
                )
                
                # Mock transcript API
                with patch('monitor.YouTubeTranscriptApi') as mock_transcript:
                    mock_transcript.get_transcript.return_value = [
                        {'text': 'Hello world', 'start': 0.0, 'duration': 2.0},
                        {'text': 'This is a test', 'start': 2.0, 'duration': 3.0}
                    ]
                    
                    transcript = monitor.get_video_transcript("test_video_id")
                    
                    assert transcript is not None
                    assert len(transcript) > 0
                    
                    print("✅ Transcript extraction successful")
                    print(f"✅ Transcript length: {len(transcript)} characters")
                    
                return True
        
    except Exception as e:
        print(f"❌ Transcript extraction test failed: {e}")
        return False

def test_data_saving():
    """Test data saving functionality."""
    print("\n💾 Testing Data Saving...")
    
    try:
        from monitor import YouTubePlaylistMonitor
        
        with patch('monitor.build') as mock_build:
            mock_youtube = Mock()
            mock_build.return_value = mock_youtube
            
            with tempfile.TemporaryDirectory() as temp_dir:
                monitor = YouTubePlaylistMonitor(
                    api_key="test_api_key",
                    playlist_id="test_playlist_id",
                    output_dir=temp_dir
                )
                
                # Test data saving
                video_id = "test_video_id"
                metadata = {
                    'title': 'Test Video',
                    'description': 'Test description',
                    'published_at': '2024-01-01T00:00:00Z'
                }
                transcript = "This is a test transcript"
                
                monitor.save_video_data(video_id, metadata, transcript)
                
                # Check that files were created
                output_path = Path(temp_dir)
                metadata_file = output_path / f"{video_id}_metadata.json"
                transcript_file = output_path / f"{video_id}_transcript.txt"
                
                assert metadata_file.exists()
                assert transcript_file.exists()
                
                print("✅ Data saving successful")
                print(f"✅ Metadata file: {metadata_file}")
                print(f"✅ Transcript file: {transcript_file}")
                
                # Test file contents
                with open(metadata_file, 'r') as f:
                    saved_metadata = json.load(f)
                    assert saved_metadata['title'] == 'Test Video'
                
                with open(transcript_file, 'r') as f:
                    saved_transcript = f.read()
                    assert transcript in saved_transcript
                
                print("✅ File contents verified")
                
                return True
        
    except Exception as e:
        print(f"❌ Data saving test failed: {e}")
        return False

def test_cli_interface():
    """Test CLI interface functionality."""
    print("\n🖥️  Testing CLI Interface...")
    
    try:
        # Test that CLI can be imported and has main function
        from cli import main as cli_main
        
        # Mock sys.argv for testing
        with patch('sys.argv', ['cli.py', '--help']):
            try:
                # This should raise SystemExit due to --help
                cli_main()
            except SystemExit:
                print("✅ CLI help functionality works")
        
        print("✅ CLI interface test successful")
        return True
        
    except Exception as e:
        print(f"❌ CLI interface test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("🎯 YouTube Monitor Script Test Suite")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Imports", test_imports()))
    test_results.append(("Configuration", test_settings_configuration()))
    test_results.append(("Monitor Initialization", test_monitor_initialization()))
    test_results.append(("Processed Videos Tracking", test_processed_videos_tracking()))
    test_results.append(("Video Metadata Extraction", test_video_metadata_extraction()))
    test_results.append(("Transcript Extraction", test_transcript_extraction()))
    test_results.append(("Data Saving", test_data_saving()))
    test_results.append(("CLI Interface", test_cli_interface()))
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    
    all_passed = True
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ YouTube Monitor Script is working correctly!")
    else:
        print("❌ Some tests failed")
        print("Please check the error messages above")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 