import os
import sys
import yt_dlp
import shutil
import eyed3

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

# Function to get the "Automatically Add to Music" directory
def get_automatically_add_to_music_dir():
    """Return the path to the 'Automatically Add to Music' folder."""
    home_dir = os.path.expanduser("~")
    auto_add_dir = os.path.join(home_dir, "Music", "Music", "Media.localized", "Automatically Add to Music.localized")
    return auto_add_dir

# Function to add metadata to the downloaded MP3 file
def add_metadata(mp3_file, artist, song_title):
    """Add artist and song title metadata to the downloaded MP3 file."""
    try:
        audio_file = eyed3.load(mp3_file)
        audio_file.tag.artist = artist
        audio_file.tag.title = song_title
        audio_file.tag.save()
        print(f"Metadata added: {artist} - {song_title}")
    except Exception as e:
        print(f"Error adding metadata to {mp3_file}: {e}")

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
            
            # Move the downloaded file to the 'Automatically Add to Music' folder
            downloaded_file = f"downloads/{title}.mp3"
            if os.path.exists(downloaded_file):
                final_path = os.path.join(auto_add_dir, f"{song_title}.mp3")
                
                # Add metadata before moving
                add_metadata(downloaded_file, artist, song_title)
                
                # Move the file to the "Automatically Add to Music" folder
                shutil.move(downloaded_file, final_path)

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
