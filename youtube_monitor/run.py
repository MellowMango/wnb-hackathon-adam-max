#!/usr/bin/env python3
"""
YouTube Playlist Monitor - Launcher

Simple launcher script for the YouTube playlist monitor.
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Launch the YouTube playlist monitor."""
    try:
        from cli import main as cli_main
        cli_main()
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 