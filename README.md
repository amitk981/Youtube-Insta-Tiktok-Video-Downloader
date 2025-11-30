# YouTube/TikTok/Instagram Downloader Bot

## Setup
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Install FFmpeg** (Required for audio conversion and high-quality video merging):
    - **Mac**: `brew install ffmpeg`
    - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.
    - **Linux**: `sudo apt install ffmpeg`
3.  **Configure Bot Token**:
    - Open `.env` and paste your token:
      ```
      BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
      ```

## Running
```bash
python bot.py
```

## Usage
- Send a link from YouTube, TikTok, or Instagram.
- Follow the on-screen buttons.
