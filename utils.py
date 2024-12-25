import os
import eyed3

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

def get_automatically_add_to_music_dir():
    """Return the path to the 'Automatically Add to Music' folder."""
    home_dir = os.path.expanduser("~")
    auto_add_dir = os.path.join(home_dir, "Music", "Music", "Media.localized", "Automatically Add to Music.localized")
    return auto_add_dir
