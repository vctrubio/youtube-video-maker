import os
from pytube import YouTube
from pydub import AudioSegment

def youtube_to_mp3(url, output_dir):
    try:
        # Download the video
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        print(f"Downloading: {yt.title}")
        output_file = video.download(output_path=output_dir)
        
        # Convert to MP3
        base, ext = os.path.splitext(output_file)
        mp3_file = base + '.mp3'
        print(f"Converting to MP3...")
        audio = AudioSegment.from_file(output_file)
        audio.export(mp3_file, format="mp3")
        
        # Remove the original video file
        os.remove(output_file)
        print(f"Saved MP3 to: {mp3_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")
    desktop_dir = os.path.expanduser("~/Desktop")
    youtube_to_mp3(url, desktop_dir)
