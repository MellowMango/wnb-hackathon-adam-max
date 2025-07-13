#!/usr/bin/env python3
"""
YouTube Video Monitor - Main Entry Point

This is the main entry point for the YouTube video monitor application.
Process individual YouTube videos to extract metadata and transcripts.
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