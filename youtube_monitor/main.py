#!/usr/bin/env python3
"""
YouTube Playlist Monitor - Main Entry Point

This is the main entry point for the YouTube playlist monitor application.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main entry point for the application."""
    
    # Import and run the CLI
    from cli import main as cli_main
    cli_main()

if __name__ == "__main__":
    main() 