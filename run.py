import os
import sys
import yt_dlp
import shutil

# Function to clean the title and artist
def get_artist_and_title(title):
    """Clean and split the YouTube video title to extract artist and song title."""
    parts = title.split('-')
    if len(parts) > 1:
        artist = parts[0].strip()
        song_title = parts[1].strip()
    else:
        artist = parts[0].strip()
        song_title = parts[0].strip()
    return artist, song_title

# Function to get the iTunes directory
def get_itunes_dir():
    """Return the path to the iTunes music directory."""
    home_dir = os.path.expanduser("~")
    itunes_dir = os.path.join(home_dir, "Music", "Music", "Media.localized", "Music")
    return itunes_dir

# Function to download audio from YouTube
def download_audio(youtube_url):
    """Download audio from a YouTube URL and move it to the iTunes music directory."""
    try:
        # Get the iTunes directory
        itunes_dir = get_itunes_dir()

        # Debugging: Print the iTunes directory for validation
        print(f"Looking for iTunes directory at: {itunes_dir}")
        
        if not os.path.exists(itunes_dir):
            print(f"Error: iTunes music directory not found at {itunes_dir}.")
            return

        # Download the video in audio format using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
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
            
            # Create artist folder if it doesn't exist
            artist_folder = os.path.join(itunes_dir, artist)
            if not os.path.exists(artist_folder):
                os.makedirs(artist_folder)

            # Move the downloaded file to iTunes Music directory
            downloaded_file = f"downloads/{title}.mp3"
            if os.path.exists(downloaded_file):
                final_path = os.path.join(artist_folder, f"{song_title}.mp3")
                shutil.move(downloaded_file, final_path)

                print(f"Successfully downloaded and saved {artist} - {song_title} to iTunes!")
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
