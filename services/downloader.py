import yt_dlp
import os
import asyncio

class Downloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'quiet': True,
            'writethumbnail': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_creator', 'android', 'ios'],
                },
            },
            'merge_output_format': 'mp4',
        }

    async def get_info(self, url):
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            return await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))

    async def download_video(self, url, quality='best', progress_hook=None):
        opts = self.ydl_opts.copy()
        
        if progress_hook:
            opts['progress_hooks'] = [progress_hook]

        if quality == 'audio':
            opts['format'] = 'bestaudio/best'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        elif quality != 'best':
             opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'
        
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=True))
            filename = ydl.prepare_filename(info)
            
            # Handle thumbnail
            thumbnail_path = None
            if info.get('thumbnail'):
                # yt-dlp saves thumbnail as filename.jpg/webp etc.
                # We need to find it.
                base_filename = os.path.splitext(filename)[0]
                for ext in ['jpg', 'jpeg', 'png', 'webp']:
                    potential_thumb = f"{base_filename}.{ext}"
                    if os.path.exists(potential_thumb):
                        thumbnail_path = potential_thumb
                        break

            if quality == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'
                
            return filename, info.get('title'), thumbnail_path

downloader = Downloader()
