# YouTube Playlist Monitor

A Python application that monitors YouTube playlists for new videos and automatically extracts their transcriptions and metadata, saving the information to organized text files.

## 🚀 Features

- **Continuous Monitoring**: Automatically checks for new videos in YouTube playlists
- **Transcript Extraction**: Gets full transcripts from YouTube videos
- **Metadata Collection**: Extracts comprehensive video information (views, likes, comments, etc.)
- **Organized Storage**: Saves data in structured text files with timestamps
- **Duplicate Prevention**: Tracks processed videos to avoid re-processing
- **Comprehensive Logging**: Detailed logging for monitoring and debugging
- **CLI Interface**: Easy-to-use command-line interface
- **Configuration Management**: Flexible configuration via environment variables or files

## 📁 Project Structure

```
youtube_monitor/
├── src/                    # Core source code
│   ├── __init__.py
│   ├── monitor.py         # Main monitoring functionality
│   └── cli.py            # Command-line interface
├── config/                # Configuration management
│   ├── __init__.py
│   └── settings.py       # Settings and configuration
├── examples/              # Usage examples
│   └── basic_usage.py    # Basic usage example
├── tests/                 # Test files
│   └── test_monitor.py   # Unit tests
├── docs/                  # Documentation
├── main.py               # Main entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🛠️ Installation

1. **Clone or download** this repository
2. **Navigate to the project directory**:
   ```bash
   cd youtube_monitor
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Get a YouTube Data API Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3
   - Create credentials (API Key)
   - Copy your API key

5. **Get your Playlist ID**:
   - Go to the YouTube playlist you want to monitor
   - Copy the URL (e.g., `https://www.youtube.com/playlist?list=PLxxxxxxxxxx`)
   - Extract the playlist ID (the part after `list=`, e.g., `PLxxxxxxxxxx`)

## ⚙️ Configuration

### Option 1: Environment Variables (Recommended)

Create a `.env` file in the project directory:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
PLAYLIST_ID=your_playlist_id_here
CHECK_INTERVAL=300
OUTPUT_DIRECTORY=youtube_data
```

### Option 2: Command Line Arguments

Use command-line arguments to specify configuration:

```bash
python main.py --api-key YOUR_API_KEY --playlist-id YOUR_PLAYLIST_ID
```

## 🎯 Usage

### Quick Start

Run the monitor with default settings:

```bash
python main.py
```

### Advanced Usage

```bash
# Run with custom parameters
python main.py --api-key YOUR_API_KEY --playlist-id YOUR_PLAYLIST_ID

# Run once without continuous monitoring
python main.py --one-time

# Custom check interval (10 minutes)
python main.py --check-interval 600

# Verbose logging
python main.py --verbose

# Custom output directory
python main.py --output-dir my_data
```

### Programmatic Usage

```python
from src.monitor import YouTubePlaylistMonitor

# Create monitor
monitor = YouTubePlaylistMonitor(
    api_key="your_api_key",
    playlist_id="your_playlist_id",
    output_dir="output_data"
)

# Check for new videos
new_videos = monitor.check_for_new_videos()

# Process videos
for video in new_videos:
    monitor.process_video(video)
```

## 📊 Output Structure

The application creates organized files for each video:

```
youtube_data/
├── processed_videos.json          # Tracks processed videos
├── video_id_20231201_143022/     # Video-specific directory
│   ├── metadata.json             # Complete video metadata
│   ├── transcript.txt            # Full transcript with headers
│   └── summary.txt               # Human-readable summary
└── youtube_monitor.log           # Application logs
```

### Sample Output Files

**metadata.json**:
```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up",
  "description": "The official music video for \"Never Gonna Give You Up\"...",
  "published_at": "2009-10-25T06:57:33Z",
  "channel_title": "Rick Astley",
  "duration": "PT3M33S",
  "view_count": "1234567890",
  "like_count": "12345678",
  "comment_count": "123456"
}
```

**transcript.txt**:
```
Video ID: dQw4w9WgXcQ
Title: Rick Astley - Never Gonna Give You Up
Published: 2009-10-25T06:57:33Z
Channel: Rick Astley
Duration: PT3M33S
Views: 1234567890
Likes: 12345678
Comments: 123456
================================================================================

[Music]
We're no strangers to love
You know the rules and so do I
A full commitment's what I'm thinking of
...
```

## 🔧 Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CHECK_INTERVAL` | 300 | Seconds between playlist checks |
| `OUTPUT_DIRECTORY` | `youtube_data` | Directory to save extracted data |
| `YOUTUBE_API_KEY` | Required | Your YouTube Data API key |
| `PLAYLIST_ID` | Required | YouTube playlist ID to monitor |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## 📈 API Quota Considerations

The YouTube Data API has daily quotas:
- **Free tier**: 10,000 units per day
- **Each API call**: 1-5 units depending on the endpoint

**Estimated usage**:
- Playlist check: ~1 unit per call
- Video metadata: ~1 unit per video
- With 5-minute intervals: ~288 units per day
- With 100 videos in playlist: ~100 units per initial scan

**Recommendations**:
- Use 5-15 minute intervals for monitoring
- Monitor playlists with < 1000 videos
- Consider upgrading API quota for high-volume usage

## 🧪 Testing

Run the test suite:

```bash
python tests/test_monitor.py
```

Or run with pytest:

```bash
pytest tests/
```

## 📝 Examples

See the `examples/` directory for usage examples:

```bash
python examples/basic_usage.py
```

## 🐛 Troubleshooting

### Common Issues

1. **"API key not valid"**
   - Verify your API key is correct
   - Ensure YouTube Data API v3 is enabled
   - Check if you've exceeded your quota

2. **"Playlist not found"**
   - Verify the playlist ID is correct
   - Ensure the playlist is public or you have access
   - Check if the playlist URL is valid

3. **"No transcript available"**
   - Not all videos have transcripts
   - Videos may have disabled captions
   - Some videos may be private or restricted

4. **"Rate limit exceeded"**
   - Increase the check interval
   - Upgrade your API quota
   - Wait for quota reset (daily)

### Log Files

Check `youtube_monitor.log` for detailed error information:

```bash
tail -f youtube_monitor.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the log files
3. Open an issue with detailed information

---

**Note**: This application respects YouTube's Terms of Service and API usage limits. Please ensure your usage complies with YouTube's policies. 