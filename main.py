"""
YouTube Audio Downloader - Main Entry Point

Simple entry point that accepts YouTube URLs as command line arguments
and downloads them as MP3 files with metadata.

Usage:
    python3 main.py "https://www.youtube.com/watch?v=VIDEO_ID"
    python3 main.py "URL1" "URL2" "URL3"  # Multiple URLs
"""

import sys
from args_of_urls import download_multiple_audio

if __name__ == "__main__":
    # Check if at least one URL was provided
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <YouTube URL(s)>")
        sys.exit(1)
    
    # Get all URLs from command line arguments (skip script name)
    youtube_urls = sys.argv[1:]
    
    # Start the download process
    download_multiple_audio(youtube_urls)