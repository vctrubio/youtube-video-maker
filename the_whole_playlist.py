import os
import sys
import yt_dlp
from datetime import datetime
import shutil
from utils import add_metadata, get_artist_and_title, get_automatically_add_to_music_dir

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

# Function to display a batch of videos in a user-friendly way
def pretty_print_batch(playlist, start_index, batch_size=50):
    print("\nFetching Playlist (Batch)...")
    print("=" * 50)
    end_index = min(start_index + batch_size, len(playlist))
    for idx in range(start_index, end_index):
        print(f"{idx + 1}. {playlist[idx]['title']}")
    print("=" * 50)
    return end_index

# Function to confirm with the user before downloading each batch
def confirm_download_batch(playlist, start_index):
    batch_size = 50
    end_index = pretty_print_batch(playlist, start_index, batch_size)
    confirmation = input(f"\nThis batch contains {end_index - start_index} videos. Do you want to download this batch? (y/n): ").lower()
    
    if confirmation != 'y':
        print("Download canceled.")
        sys.exit(0)
    
    # Ask user for the batch size for the next batch
    batch_size = int(input("Enter the batch size for the next set of videos: "))
    return end_index, batch_size

# Function to download a batch of videos
def download_batch(playlist, start_index, batch_size=50):
    try:
        # Get the download directory from utils
        download_path = get_automatically_add_to_music_dir()
        
        # Ensure the download directory exists
        if not os.path.exists(download_path):
            print(f"Creating download directory at: {download_path}")
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
            # Perform the download of the selected batch of videos
            ydl.download([entry['url'] for entry in playlist[start_index:start_index + batch_size]])

        # Add metadata to each downloaded file
        for entry in playlist[start_index:start_index + batch_size]:
            title = entry.get('title', '')
            artist, song_title = get_artist_and_title(title)
            downloaded_file = os.path.join(download_path, f"{title}.mp3")
            if os.path.exists(downloaded_file):
                add_metadata(downloaded_file, artist, song_title)

        print(f"\nBatch download finished. Videos saved to {download_path}.\n")
    except Exception as e:
        print(f"An error occurred while downloading the batch: {str(e)}")

# Main function to handle playlist download
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 run.py <YouTube Song URL>")
        sys.exit(1)

    youtube_url = sys.argv[1]

    # Step 1: Get playlist from the song URL
    playlist = get_playlist_from_song(youtube_url)

    if playlist:
        start_index = 0
        batch_size = 10
        total_videos = len(playlist)

        while start_index < total_videos:
            # Step 2: Confirm download for the current batch
            start_index, batch_size = confirm_download_batch(playlist, start_index)

            # Step 3: Download the current batch
            download_batch(playlist, start_index - batch_size, batch_size)

            # If there are more videos, continue
            if start_index < total_videos:
                more_to_download = input(f"{total_videos - start_index} videos remaining. Do you want to download the next batch? (y/n): ").lower()
                if more_to_download != 'y':
                    print("Download canceled.")
                    break

if __name__ == "__main__":
    main()
