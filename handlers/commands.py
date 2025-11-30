from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Welcome to the Video Downloader Bot! 📥\n\n"
        "I can download videos from:\n"
        "🎥 **YouTube**\n"
        "🎵 **TikTok**\n"
        "📸 **Instagram**\n\n"
        "Just send me a link and I'll do the rest!"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "How to use:\n"
        "1. Send a YouTube link.\n"
        "2. Choose format (Video/Audio).\n"
        "3. Choose quality.\n"
        "4. Wait for the file!"
    )
