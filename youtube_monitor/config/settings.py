"""
YouTube Playlist Monitor - Configuration Settings

This module handles configuration settings for the YouTube playlist monitor.
"""

import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, continue without it
    pass

class Settings:
    """Configuration settings for the YouTube playlist monitor."""
    
    def __init__(self):
        """Initialize settings from environment variables."""
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY', '')
        self.playlist_id = os.getenv('PLAYLIST_ID', '')
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '300'))
        self.output_directory = os.getenv('OUTPUT_DIRECTORY', 'youtube_data')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        
        # Default playlist IDs for examples
        self.example_playlists = {
            'tech_tutorials': 'PLrAXtmRdnEQyWXj5QjqHhqKqQqQqQqQqQq',  # Replace with actual ID
            'music_videos': 'PLrAXtmRdnEQyWXj5QjqHhqKqQqQqQqQqQq',   # Replace with actual ID
            'news_updates': 'PLrAXtmRdnEQyWXj5QjqHhqKqQqQqQqQqQq'   # Replace with actual ID
        }
    
    def validate(self) -> bool:
        """Validate that required settings are present."""
        if not self.youtube_api_key:
            print("❌ Error: YOUTUBE_API_KEY not set")
            return False
        
        if not self.playlist_id:
            print("❌ Error: PLAYLIST_ID not set")
            return False
        
        return True
    
    def get_output_path(self) -> Path:
        """Get the output directory path."""
        return Path(self.output_directory)
    
    def print_config(self):
        """Print current configuration."""
        print("📋 Configuration:")
        print(f"  API Key: {'✅ Set' if self.youtube_api_key else '❌ Not set'}")
        print(f"  Playlist ID: {self.playlist_id or '❌ Not set'}")
        print(f"  Check Interval: {self.check_interval} seconds")
        print(f"  Output Directory: {self.output_directory}")
        print(f"  Log Level: {self.log_level}")

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings

def load_from_file(config_file: str) -> bool:
    """Load settings from a configuration file."""
    try:
        config_path = Path(config_file)
        if config_path.exists():
            # Load as Python module
            import importlib.util
            spec = importlib.util.spec_from_file_location("config", config_path)
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)
            
            # Update settings from config file
            if hasattr(config_module, 'YOUTUBE_API_KEY'):
                settings.youtube_api_key = config_module.YOUTUBE_API_KEY
            if hasattr(config_module, 'PLAYLIST_ID'):
                settings.playlist_id = config_module.PLAYLIST_ID
            if hasattr(config_module, 'CHECK_INTERVAL'):
                settings.check_interval = int(config_module.CHECK_INTERVAL)
            if hasattr(config_module, 'OUTPUT_DIRECTORY'):
                settings.output_directory = config_module.OUTPUT_DIRECTORY
            
            return True
    except Exception as e:
        print(f"❌ Error loading config file: {e}")
        return False
    
    return False 