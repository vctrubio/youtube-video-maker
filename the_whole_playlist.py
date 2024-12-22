import os
import sys
import yt_dlp
from datetime import datetime
import shutil

# Function to get the playlist from a song URL
def get_playlist_from_song(youtube_url):
    try:
        # Extract info about the playlist from the song URL
        ydl_opts = {
            'quiet': True,  # Suppress unnecessary output
            'extract_flat': True,  # Only get the playlist info (no actual download yet)
            'force_generic_extractor': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(youtube_url, download=False)

        if 'entries' not in result:
            print("No playlist found for this song URL.")
            return None
        return result['entries']
    except Exception as e:
        print(f"An error occurred while fetching playlist info: {str(e)}")
        return None

# Function to display the playlist in a user-friendly way
def pretty_print_playlist(playlist):
    print("\nFetching Playlist...")
    print("=" * 50)
    for idx, video in enumerate(playlist, 1):
        print(f"{idx}. {video['title']}")
    print("=" * 50)

# Function to confirm with the user before downloading the playlist
def confirm_download(playlist):
    pretty_print_playlist(playlist)
    confirmation = input(f"\nThis playlist has {len(playlist)} videos. Do you want to download this playlist? (y/n): ").lower()
    
    if confirmation != 'y':
        print("Download canceled.")
        sys.exit(0)

# Function to download the playlist
def download_playlist(playlist, download_path='downloads'):
    try:
        # Ensure the download directory exists
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        # Options for downloading the videos
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': False,  # Allow downloading the entire playlist
            'quiet': False,  # Print progress
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Perform the download of the whole playlist
            ydl.download([entry['url'] for entry in playlist])

        print(f"\nDownload finished. All videos saved to {download_path}.\n")
    except Exception as e:
        print(f"An error occurred while downloading the playlist: {str(e)}")

# Main function to handle playlist download
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 run.py <YouTube Song URL>")
        sys.exit(1)

    youtube_url = sys.argv[1]

    # Step 1: Get playlist from the song URL
    playlist = get_playlist_from_song(youtube_url)

    if playlist:
        # Step 2: Confirm download
        confirm_download(playlist)
        
        # Step 3: Download the playlist
        download_playlist(playlist)

if __name__ == "__main__":
    main()
