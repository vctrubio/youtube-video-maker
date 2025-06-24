"""
YouTube Audio Downloader - Core Download Functions

This module handles the actual downloading and processing of YouTube videos,
converting them to MP3 format with metadata.

Configuration:
    LOCATION_SAVE: Directory where downloaded MP3 files will be saved
    
Functions:
    download_audio(youtube_url): Download single URL
    download_multiple_audio(youtube_urls): Download multiple URLs with progress tracking
"""

import os
import sys
import yt_dlp
from utils import (
    add_metadata,
    get_artist_and_title
)

# Configure download location - change this path as needed
# Default: ~/Music/Automatically Add to Music (works with iTunes on macOS)
LOCATION_SAVE = os.path.expanduser("~/Music/Automatically Add to Music")

def download_audio(youtube_url):
    """
    Download audio from a single YouTube URL and convert to MP3 with metadata.
    
    Args:
        youtube_url (str): The YouTube URL to download
        
    Returns:
        bool: True if download successful, False otherwise
    """
    try:
        print(f"Using download directory: {LOCATION_SAVE}")

        # Create download directory if it doesn't exist
        if not os.path.exists(LOCATION_SAVE):
            os.makedirs(LOCATION_SAVE, exist_ok=True)

        # Configure yt-dlp options for high-quality MP3 download
        ydl_opts = {
            'format': 'bestaudio/best',                               # Best audio quality available
            'outtmpl': os.path.join(LOCATION_SAVE, '%(id)s.%(ext)s'), # Use video ID for filename
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',                          # Convert to audio only
                'preferredcodec': 'mp3',                              # Output format: MP3
                'preferredquality': '192',                            # 192kbps quality
            }],
            'noplaylist': True,                                       # Download single video only
            'ignoreerrors': True,                                     # Continue on errors
            'retries': 10,                                           # Retry failed downloads
            'fragment-retries': 10,                                  # Retry failed fragments
            'http-chunk-size': 10485760,                             # 10MB chunks for stability
            'verbose': False,                                        # Quiet output
            'postprocessor_args': ['-loglevel', 'error'],           # Suppress FFmpeg output
            'headers': {                                             # Headers to avoid blocking
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                'Referer': 'https://www.youtube.com/'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information without downloading first
            info_dict = ydl.extract_info(youtube_url, download=False)
            
            # Validate required fields exist
            if 'id' not in info_dict:
                raise ValueError("Could not extract video ID from URL")
            
            video_id = info_dict['id']
            title = info_dict.get('title', 'Donkey Drills Dev')
            print(f"Downloading: {title}")
            
            # Start actual download process
            ydl.process_info(info_dict)
            
            # Check if the downloaded MP3 file exists
            downloaded_file = os.path.join(LOCATION_SAVE, f"{video_id}.mp3")
            
            if os.path.exists(downloaded_file):
                # Extract artist and title from video title
                artist, song_title = get_artist_and_title(title)
                
                # Add ID3 metadata tags to the MP3 file
                add_metadata(downloaded_file, artist, song_title)
                print(f"Successfully processed: {artist} - {song_title}")
                return True
            else:
                print(f"Download failed for: {youtube_url}")
                return False

    except yt_dlp.utils.DownloadError as e:
        print(f"Download error: {str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

def download_multiple_audio(youtube_urls):
    """
    Download audio from multiple YouTube URLs with progress tracking.
    
    Args:
        youtube_urls (list): List of YouTube URLs to download
        
    Prints progress and final success rate to console.
    """
    success_count = 0
    total = len(youtube_urls)
    
    # Process each URL with progress indication
    for idx, url in enumerate(youtube_urls, 1):
        print(f"\nProcessing URL {idx}/{total}: {url}")
        if download_audio(url):
            success_count += 1
    
    # Print final summary
    print(f"\nDownload complete. Success: {success_count}/{total}")

# Allow this file to be run directly as an alternative to main.py
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 args_of_urls.py <YouTube URL(s)>")
        sys.exit(1)
    
    # Get URLs from command line and start download
    youtube_urls = sys.argv[1:]
    download_multiple_audio(youtube_urls)
