"""
Utility Functions for YouTube Audio Downloader

This module provides helper functions for:
- Adding ID3 metadata tags to MP3 files
- Parsing YouTube video titles to extract artist and song information
"""

import os
import eyed3

def add_metadata(mp3_file, artist, song_title):
    """
    Add ID3 metadata tags (artist and title) to an MP3 file.
    
    Args:
        mp3_file (str): Path to the MP3 file
        artist (str): Artist name to set in metadata
        song_title (str): Song title to set in metadata
        
    Prints success/error message to console.
    """
    try:
        # Load the MP3 file for metadata editing
        audio_file = eyed3.load(mp3_file)
        
        # Set the artist and title tags
        audio_file.tag.artist = artist
        audio_file.tag.title = song_title
        
        # Save the metadata to the file
        audio_file.tag.save()
        print(f"Metadata added: {artist} - {song_title}")
    except Exception as e:
        print(f"Error adding metadata to {mp3_file}: {e}")

def get_artist_and_title(title):
    """
    Parse a YouTube video title to extract artist and song title.
    
    Expects format: "Artist - Song Title" or uses the full title for both
    if no dash separator is found.
    
    Args:
        title (str): The YouTube video title
        
    Returns:
        tuple: (artist, song_title) - both as strings
        
    Example:
        "The Beatles - Hey Jude" -> ("The Beatles", "Hey Jude")
        "Amazing Song" -> ("Amazing Song", "Amazing Song")
    """
    # Split on dash character (common format: "Artist - Song")
    parts = title.split('-')
    
    if len(parts) > 1:
        # Found dash separator - use first part as artist, rest as title
        artist = parts[0].strip()
        song_title = parts[1].strip()
    else:
        # No dash found - use full title for both artist and song
        artist = parts[0].strip()
        song_title = parts[0].strip()
    
    return artist, song_title

