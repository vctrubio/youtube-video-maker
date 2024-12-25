import os
import sys
import yt_dlp
import shutil
from utils import add_metadata, get_artist_and_title, get_automatically_add_to_music_dir

# Function to download audio from YouTube
def download_audio(youtube_url):
    """Download audio from a YouTube URL and move it to the 'Automatically Add to Music' folder."""
    try:
        # Get the 'Automatically Add to Music' directory
        auto_add_dir = get_automatically_add_to_music_dir()

        # Debugging: Print the "Automatically Add to Music" directory for validation
        print(f"Looking for 'Automatically Add to Music' directory at: {auto_add_dir}")
        
        if not os.path.exists(auto_add_dir):
            print(f"Error: 'Automatically Add to Music' directory not found at {auto_add_dir}.")
            return

        # Download the video in audio format using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(auto_add_dir, '%(title)s.%(ext)s'),  # Save directly to the target directory
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,  # Prevent downloading playlists
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(youtube_url, download=True)

            # Extract title, artist, and song title
            title = result.get('title', '')
            artist, song_title = get_artist_and_title(title)

            # Handle missing artist or title
            if not artist or not song_title:
                artist = "Unknown Artist"
                song_title = "Unknown Title"
            
            # Path to the downloaded file
            downloaded_file = os.path.join(auto_add_dir, f"{title}.mp3")
            if os.path.exists(downloaded_file):
                # Add metadata before moving
                add_metadata(downloaded_file, artist, song_title)

                print(f"Successfully downloaded and saved {artist} - {song_title} to 'Automatically Add to Music'!")
            else:
                print(f"Error: Downloaded file '{downloaded_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Main function to handle multiple YouTube URLs
def download_multiple_audio(youtube_urls):
    """Download audio for multiple YouTube URLs."""
    for youtube_url in youtube_urls:
        print(f"Downloading audio for: {youtube_url}")
        download_audio(youtube_url)

# Main function to get the URL(s) from command line argument(s)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run.py <YouTube URL(s)>")
    else:
        youtube_urls = sys.argv[1:]
        download_multiple_audio(youtube_urls)
