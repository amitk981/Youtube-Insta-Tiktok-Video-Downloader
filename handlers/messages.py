from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, BufferedInputFile
from services.downloader import downloader
from utils.progress import ProgressFileReader
import os
import time
import asyncio

router = Router()

# Regex patterns for supported platforms
YOUTUBE_PATTERN = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+'
TIKTOK_PATTERN = r'(https?://)?(www\.)?(tiktok)\.com/.+'
INSTAGRAM_PATTERN = r'(https?://)?(www\.)?(instagram)\.com/.+'

@router.message(F.text.regexp(YOUTUBE_PATTERN))
async def handle_youtube_url(message: Message):
    await message.reply(
        "YouTube link detected! 📹\nChoose format:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Video (Best)", callback_data=f"dl_video_best")],
            [InlineKeyboardButton(text="Video (720p)", callback_data=f"dl_video_720")],
            [InlineKeyboardButton(text="Audio (MP3)", callback_data=f"dl_audio")]
        ])
    )

@router.message(F.text.regexp(TIKTOK_PATTERN))
async def handle_tiktok_url(message: Message):
    await message.reply(
        "TikTok link detected! 🎵\nDownloading without watermark...",
    )
    await process_download(message, message.text, "best")

@router.message(F.text.regexp(INSTAGRAM_PATTERN))
async def handle_instagram_url(message: Message):
    await message.reply(
        "Instagram link detected! 📸\nDownloading...",
    )
    await process_download(message, message.text, "best")

@router.callback_query(F.data.startswith("dl_"))
async def handle_callback(callback: CallbackQuery):
    action = callback.data.split("_")[1] # video or audio
    quality = callback.data.split("_")[2] if len(callback.data.split("_")) > 2 else "best"
    
    if callback.message.reply_to_message:
        url = callback.message.reply_to_message.text
        await callback.message.edit_text(f"Downloading {action} ({quality})...")
        await process_download(callback.message, url, quality if action == 'video' else 'audio')
    else:
        await callback.message.edit_text("Error: Could not find original link.")

async def process_download(message: Message, url: str, quality: str):
    status_msg = await message.answer("Initializing download... 0%")
    last_update_time = 0

    def progress_hook(d):
        nonlocal last_update_time
        if d['status'] == 'downloading':
            current_time = time.time()
            if current_time - last_update_time > 2: # Update every 2 seconds
                percent = d.get('_percent_str', '0%').strip()
                try:
                    # Use create_task to avoid blocking the download thread
                    asyncio.create_task(status_msg.edit_text(f"Downloading... {percent} ⬇️"))
                    last_update_time = current_time
                except Exception:
                    pass

    try:
        file_path, title, thumbnail_path = await downloader.download_video(url, quality, progress_hook)
        
        # Check file size (Telegram limit 50MB for bots without local server)
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        if file_size > 50 * 1024 * 1024:
            await status_msg.edit_text(f"⚠️ File is too large ({file_size_mb:.1f}MB). Telegram bots can only send up to 50MB directly.")
            os.remove(file_path)
            if thumbnail_path and os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            return

        # Real-time upload progress
        async def upload_progress(current, total):
            percent = (current / total) * 100
            uploaded_mb = current / (1024 * 1024)
            total_mb = total / (1024 * 1024)
            
            try:
                # Update every 5% or 3 seconds (handled by wrapper)
                await status_msg.edit_text(
                    f"Uploading... {percent:.1f}% ⬆️\n"
                    f"({uploaded_mb:.1f}MB / {total_mb:.1f}MB)"
                )
            except Exception:
                pass

        try:
            # We use BufferedInputFile with our custom reader
            # But BufferedInputFile expects bytes, not a file-like object usually?
            # Actually FSInputFile is path-based. BufferedInputFile takes bytes.
            # aiogram doesn't expose a way to pass a file-like object directly to FSInputFile.
            # However, we can use BufferedInputFile(file, filename=...) where file is our reader.
            # Let's verify if BufferedInputFile accepts a binary IO. 
            # Yes, it accepts bytes or BinaryIO.
            
            reader = ProgressFileReader(file_path, upload_progress)
            
            # Note: BufferedInputFile reads the whole file into memory if passed bytes, 
            # but if passed an IO object, it *should* stream it.
            # Wait, aiogram's BufferedInputFile might read it all.
            # Let's check if we can pass the reader to FSInputFile? No, FSInputFile takes a path.
            # We have to use BufferedInputFile with the reader.
            
            media_file = BufferedInputFile(reader, filename=os.path.basename(file_path))
            thumbnail_file = FSInputFile(thumbnail_path) if thumbnail_path else None

            if quality == 'audio':
                await message.answer_audio(media_file, caption=title, thumbnail=thumbnail_file)
            else:
                await message.answer_video(media_file, caption=title, thumbnail=thumbnail_file, width=1280, height=720)
            
            reader.close()
            
        finally:
            pass
            
        await status_msg.delete()
        
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
        if thumbnail_path and os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        
    except Exception as e:
        await status_msg.edit_text(f"Error: {str(e)}")
