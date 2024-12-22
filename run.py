import os
import argparse
from yt_dlp import YoutubeDL

def fetch_video_details(url):
    """Fetch and display video details using yt-dlp."""
    try:
        ydl_opts = {'quiet': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"Video Title: {info['title']}")
            print(f"Author: {info['uploader']}")
            print(f"Views: {info['view_count']}")
            print(f"Duration: {info['duration'] // 60} minutes {info['duration'] % 60} seconds")
            return info
    except Exception as e:
        print(f"Error fetching video details: {e}")
        return None

def download_audio(url, output_dir):
    """Download audio using yt-dlp."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Audio downloaded successfully!")
    except Exception as e:
        print(f"Error downloading audio: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch YouTube video details and download audio.")
    parser.add_argument("url", help="The URL of the YouTube video")
    args = parser.parse_args()

    # Output directory
    desktop_dir = os.path.expanduser("~/Desktop")

    # Fetch video details
    video_info = fetch_video_details(args.url)
    if video_info:
        # Proceed to download only if video details are fetched successfully
        download_audio(args.url, desktop_dir)
