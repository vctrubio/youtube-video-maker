# Donkey Drills Dev - YouTube Audio Downloader

A Python script for downloading audio from YouTube videos and automatically adding metadata.

## Project Structure

```
youtube_api/
├── main.py                 # Main entry point (recommended)
├── args_of_urls.py         # Core download functions (can also be run directly)
├── utils.py                # Helper functions for metadata and file handling
├── the_whole_playlist.py   # Playlist downloader (BETA - has issues)
├── requirements.txt        # Python dependencies
├── Makefile               # Installation and setup commands
└── readme.md              # This file
```

### File Descriptions

- **`main.py`** - Simple entry point that calls the download functions
- **`args_of_urls.py`** - Contains all the download logic and can be run standalone
- **`utils.py`** - Helper functions for adding metadata and parsing titles
- **`the_whole_playlist.py`** - Beta playlist downloader (currently broken)
- **`requirements.txt`** - Lists required Python packages (yt-dlp, eyed3)
- **`Makefile`** - Provides easy installation with `make install`

## Prerequisites

- Python 3.6 or higher
- FFmpeg (for audio conversion)

### Install Python

If you don't have Python 3 installed, download it from [python.org](https://www.python.org/downloads/)

### Install FFmpeg

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## Installation

1. Clone or download this repository
2. Install dependencies using the Makefile:

```bash
make install
```

This will:
- Check if Python 3 is installed
- Install required Python packages (yt-dlp, eyed3)

## Usage

### Download a single song

```bash
python3 main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download multiple songs

You can download multiple songs by providing multiple URLs as arguments:

```bash
python3 main.py \
  "https://www.youtube.com/watch?v=VIDEO_ID1" \
  "https://www.youtube.com/watch?v=VIDEO_ID2" \
  "https://www.youtube.com/watch?v=VIDEO_ID3"
```

### Example with real URLs

```bash
# Single song
python3 main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Multiple songs
python3 main.py \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  "https://www.youtube.com/watch?v=L_jWHffIx5E" \
  "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"
```

## Configuration

### Changing Download Location

By default, files are saved to `~/Music/Automatically Add to Music`. To change this:

1. Open `args_of_urls.py`
2. Find the line: `LOCATION_SAVE = os.path.expanduser("~/Music/Automatically Add to Music")`
3. Change the path to your preferred location:
   ```python
   LOCATION_SAVE = os.path.expanduser("~/Downloads")  # Example: Downloads folder
   ```

### Common Download Locations
- **iTunes (macOS)**: `~/Music/Automatically Add to Music` (default)
- **Downloads**: `~/Downloads`
- **Desktop**: `~/Desktop`
- **Custom**: `/path/to/your/music/folder`

## Features

- Downloads audio in MP3 format (192kbps quality)
- Automatically extracts artist and title from video title
- Adds ID3 metadata to downloaded files
- Configurable download location
- Progress tracking for multiple downloads
- Error handling and retry logic
- Works with individual videos or multiple URLs

## Optional: Create an Alias for Easy Access

For convenience, you can create an alias to run the script from anywhere:

1. **Find your project path** (replace with your actual path):
```bash
pwd
# Example output: /Users/username/kode/projects/scraping_scripts/youtube_api
```

2. **Add alias to your shell profile**:

**For zsh (macOS default):**
```bash
echo "alias ytd='python3 /Users/username/kode/projects/scraping_scripts/youtube_api/args_of_urls.py'" >> ~/.zshrc
source ~/.zshrc
```

**For bash:**
```bash
echo "alias ytd='python3 /Users/username/kode/projects/scraping_scripts/youtube_api/args_of_urls.py'" >> ~/.bashrc
source ~/.bashrc
```

3. **Replace the path** in the command above with your actual project path from step 1

4. **Now you can use it anywhere:**
```bash
# Single song
ytd "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Multiple songs
ytd "https://www.youtube.com/watch?v=URL1" "https://www.youtube.com/watch?v=URL2"
```

### 💡 Pro Tip for Mac Users with iTerm2
If you use iTerm2, you can enable ultra-fast downloads:
1. **Set up hotkey**: Go to iTerm2 → Preferences → Keys → Hotkey → Create a Dedicated Hotkey Window
2. **Use Ctrl+Enter** to instantly open terminal overlay
3. **Type your alias**: `ytd ` then paste the YouTube URL
4. **Hit Enter** for instant download

This creates a lightning-fast workflow: Copy YouTube URL → Ctrl+Enter → `ytd <paste>` → Enter → Done!

## Other Commands

```bash
# Show available make targets
make help

# Clean up cache files
make clean
```

## Beta Features

### Playlist Downloader (BETA)

There is also a [`the_whole_playlist.py`](the_whole_playlist.py) script for downloading entire playlists, but **this is currently in BETA** and has known issues:

⚠️ **Known Issues:**
- Song scoping does NOT work correctly
- May download unexpected content
- Use at your own risk

## How It Works

1. **Download**: Uses `yt-dlp` to download the best available audio from YouTube
2. **Convert**: Automatically converts to MP3 format at 192kbps quality
3. **Parse**: Extracts artist and song title from the video title (expects "Artist - Song" format)
4. **Metadata**: Adds ID3 tags (artist, title) to the MP3 file using `eyed3`
5. **Save**: Places the final MP3 in your configured download location

## Notes

- Video titles in "Artist - Song Title" format work best for metadata extraction
- Files are initially saved with the YouTube video ID, then processed and tagged
- Requires FFmpeg for audio conversion (installed via `make install` instructions)
- Works with most YouTube videos that have downloadable audio
