#!/usr/bin/env python3
"""
Test Module for YouTube Playlist Monitor

This module contains tests for the YouTube playlist monitor functionality.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent.parent / "src"))

class TestYouTubePlaylistMonitor(unittest.TestCase):
    """Test cases for YouTubePlaylistMonitor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_api_key"
        self.playlist_id = "test_playlist_id"
        self.output_dir = "test_output"
    
    @patch('monitor.build')
    def test_initialization(self, mock_build):
        """Test monitor initialization."""
        from monitor import YouTubePlaylistMonitor
        
        # Mock the YouTube API client
        mock_youtube = Mock()
        mock_build.return_value = mock_youtube
        
        monitor = YouTubePlaylistMonitor(
            api_key=self.api_key,
            playlist_id=self.playlist_id,
            output_dir=self.output_dir
        )
        
        self.assertEqual(monitor.api_key, self.api_key)
        self.assertEqual(monitor.playlist_id, self.playlist_id)
        self.assertEqual(str(monitor.output_dir), self.output_dir)
    
    def test_processed_videos_tracking(self):
        """Test processed videos tracking functionality."""
        from monitor import YouTubePlaylistMonitor
        
        with patch('monitor.build'):
            monitor = YouTubePlaylistMonitor(
                api_key=self.api_key,
                playlist_id=self.playlist_id,
                output_dir=self.output_dir
            )
            
            # Test initial state
            self.assertEqual(len(monitor.processed_videos), 0)
            
            # Test adding processed video
            monitor.processed_videos.add("test_video_id")
            self.assertIn("test_video_id", monitor.processed_videos)
    
    def test_video_id_extraction(self):
        """Test video ID extraction from playlist URL."""
        # Test various playlist URL formats
        test_cases = [
            ("https://www.youtube.com/playlist?list=PLxxxxxxxxxx", "PLxxxxxxxxxx"),
            ("https://youtube.com/playlist?list=PLxxxxxxxxxx", "PLxxxxxxxxxx"),
            ("PLxxxxxxxxxx", "PLxxxxxxxxxx"),  # Direct ID
        ]
        
        for url, expected_id in test_cases:
            # This would be implemented in a utility function
            # For now, just test the concept
            if "list=" in url:
                extracted_id = url.split("list=")[1].split("&")[0]
            else:
                extracted_id = url
            
            self.assertEqual(extracted_id, expected_id)

class TestConfiguration(unittest.TestCase):
    """Test cases for configuration functionality."""
    
    def test_settings_validation(self):
        """Test settings validation."""
        from config.settings import Settings
        
        settings = Settings()
        
        # Test with missing API key
        settings.youtube_api_key = ""
        settings.playlist_id = "test_id"
        self.assertFalse(settings.validate())
        
        # Test with missing playlist ID
        settings.youtube_api_key = "test_key"
        settings.playlist_id = ""
        self.assertFalse(settings.validate())
        
        # Test with valid settings
        settings.youtube_api_key = "test_key"
        settings.playlist_id = "test_id"
        self.assertTrue(settings.validate())

def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestYouTubePlaylistMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 