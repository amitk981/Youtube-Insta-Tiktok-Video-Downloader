# ============================================
# TELEGRAM VIDEO DOWNLOADER BOT
# ============================================
# This bot helps users download videos from YouTube, TikTok, and Instagram
# It also shows ads (Monetag) to earn money

# ============================================
# STEP 1: Import the tools we need
# ============================================
import os  # This helps us read settings from the computer
import logging  # This helps us write messages about what the bot is doing
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup  # Tools to work with Telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes  # More Telegram tools
from http.server import HTTPServer, BaseHTTPRequestHandler  # Tools to create a simple web server
from threading import Thread  # Tool to run multiple things at once

# ============================================
# STEP 2: Set up logging (like a diary for the bot)
# ============================================
# This creates a "diary" that writes down everything the bot does
# It helps us see if something goes wrong
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # How each diary entry looks
    level=logging.INFO  # Write down important things
)
logger = logging.getLogger(__name__)  # Create our diary writer

# ============================================
# STEP 3: Get important information
# ============================================
# TOKEN: This is like a password that lets our bot talk to Telegram
# We get it from the computer's settings (environment variables)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# MONETAG_LINK: This is the ad link that makes us money
# When users click it, we earn money!
MONETAG_LINK = "https://otieu.com/4/10256428"

# PORT: Render needs us to open a port (like a door for web traffic)
# We get this from Render's settings, or use 10000 as default
PORT = int(os.environ.get("PORT", 10000))

# ============================================
# STEP 3.5: Create a simple web server (for Render)
# ============================================
class HealthCheckHandler(BaseHTTPRequestHandler):
    """
    This is a simple web server that Render can check
    It's like a "I'm alive!" signal
    """
    def do_GET(self):
        # When someone visits our web address, say "Bot is running!"
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>Telegram Bot is Running!</h1><p>Bot Status: Active</p>')
    
    def log_message(self, format, *args):
        # Don't print every web request (keeps logs clean)
        return

def run_health_server():
    """
    Start the web server on the port Render expects
    This runs in the background while the bot runs
    """
    server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
    logger.info(f"Health check server running on port {PORT}")
    server.serve_forever()

# ============================================
# STEP 4: Define what happens when user sends /start
# ============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function runs when someone types /start
    It shows them a welcome message and a button with the ad link
    """
    # Get the user's ID (like their username number)
    user_id = update.effective_user.id
    
    # Write in our diary that this user started the bot
    logger.info(f"User {user_id} started the bot")
    
    # Create a button that shows the ad link
    # This is how we make money - when users click this button!
    keyboard = [
        [InlineKeyboardButton("🎁 Click here to access bot", url=MONETAG_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)  # Package the button nicely
    
    # Send the welcome message with the button
    await update.message.reply_text(
        "🎬 Welcome to Video Downloader Bot!\n\n"
        "To use this bot, please verify you are human by clicking the link below.\n"
        "After clicking, come back and send me a video URL!",
        reply_markup=reply_markup  # Include the button
    )

# ============================================
# STEP 5: Define what happens when user sends /help
# ============================================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function runs when someone types /help
    It tells them how to use the bot
    """
    await update.message.reply_text(
        "📖 How to use:\n\n"
        "1. Click the verification link from /start\n"
        "2. Send me a YouTube, TikTok, or Instagram URL\n"
        "3. I'll download and send you the video!\n\n"
        "Supported platforms:\n"
        "• YouTube\n"
        "• TikTok\n"
        "• Instagram\n"
        "• And many more!"
    )

# ============================================
# STEP 6: Define what happens when user sends a video URL
# ============================================
async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function runs when someone sends a message (not a command)
    It checks if it's a video URL and downloads the video
    """
    # Get the user's ID
    user_id = update.effective_user.id
    
    # Get the message they sent (the URL)
    url = update.message.text
    
    # Write in our diary what URL they sent
    logger.info(f"User {user_id} sent URL: {url}")
    
    # Check if the URL is from YouTube, TikTok, or Instagram
    # We look for these words in the URL
    if not any(platform in url.lower() for platform in ['youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com', 'reels']):
        # If it's not a valid URL, tell them
        await update.message.reply_text(
            "❌ Please send a valid video URL from:\n"
            "• YouTube\n"
            "• TikTok\n"
            "• Instagram"
        )
        return  # Stop here, don't do anything else
    
    # Tell the user we're starting the download
    status_message = await update.message.reply_text("⏳ Downloading video... Please wait!")
    
    try:
        # Import yt-dlp (the tool that downloads videos)
        import yt_dlp
        import os
        import tempfile
        
        # Create a temporary folder to store the video
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, 'video.%(ext)s')
        
        # Configure yt-dlp settings with YouTube bypass
        ydl_opts = {
            'format': 'best[ext=mp4][height<=480]/best[height<=480]/worst',  # Lower quality to avoid restrictions
            'outtmpl': output_path,  # Where to save the file
            'quiet': True,  # Don't print too much info
            'no_warnings': True,
            # Try to extract cookies from browser automatically
            'cookiesfrombrowser': ('chrome',),  # Try Chrome first, falls back to Firefox/Edge
            # Bypass YouTube bot detection
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'web'],  # Try multiple clients
                    'skip': ['hls', 'dash'],  # Skip certain formats
                }
            },
            # Spoof user agent to look like a real browser
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            # Ignore errors and try to continue
            'ignoreerrors': False,
            'nocheckcertificate': True,
        }
        
        # Download the video
        logger.info(f"Starting download for URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        # Update status: Download complete, now uploading
        await status_message.edit_text("✅ Download complete! Uploading to Telegram...")
        
        # Check file size (Telegram has a 50MB limit for bots)
        file_size = os.path.getsize(filename)
        if file_size > 50 * 1024 * 1024:  # 50MB in bytes
            await status_message.edit_text(
                "❌ Sorry, this video is too large (over 50MB).\n"
                "Telegram bots can only send files up to 50MB."
            )
            # Clean up the file
            os.remove(filename)
            os.rmdir(temp_dir)
            return
        
        # Send the video to the user
        logger.info(f"Uploading video to user {user_id}")
        with open(filename, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption="✅ Here's your video!\n\n💡 Share this bot with friends!",
                supports_streaming=True
            )
        
        # Delete the status message
        await status_message.delete()
        
        # Clean up: Delete the temporary file and folder
        os.remove(filename)
        os.rmdir(temp_dir)
        logger.info(f"Successfully sent video to user {user_id}")
        
    except Exception as e:
        # If something goes wrong, tell the user
        logger.error(f"Error downloading video: {str(e)}")
        await status_message.edit_text(
            f"❌ Sorry, I couldn't download this video.\n\n"
            f"Error: {str(e)[:100]}\n\n"
            f"Please try:\n"
            f"• A different video URL\n"
            f"• A shorter video\n"
            f"• A public video (not private)"
        )

# ============================================
# STEP 7: Define what happens when there's an error
# ============================================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """
    This function runs when something goes wrong
    It writes the error in our diary so we can fix it
    """
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)

# ============================================
# STEP 8: The main function - this starts everything!
# ============================================
def main():
    """
    This is the main function that starts the bot
    It's like pressing the "ON" button
    """
    # First, check if we have the bot token (password)
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return  # Stop if we don't have the password
    
    # IMPORTANT: Start the health check server FIRST
    # This lets Render detect the port immediately (fixes timeout issue)
    logger.info("Starting health check server...")
    health_thread = Thread(target=run_health_server, daemon=True)
    health_thread.start()
    
    # Give the server a moment to start
    import time
    time.sleep(2)
    logger.info(f"Health check server running on port {PORT}")
    
    # Now start the bot
    logger.info("Starting Telegram bot...")
    
    # Create the bot application (like building the bot)
    application = Application.builder().token(TOKEN).build()
    
    # Tell the bot what to do when users send different things:
    # - When they send /start, run the start() function
    application.add_handler(CommandHandler("start", start))
    
    # - When they send /help, run the help_command() function
    application.add_handler(CommandHandler("help", help_command))
    
    # - When they send any text (not a command), run the handle_url() function
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    
    # - If anything goes wrong, run the error_handler() function
    application.add_error_handler(error_handler)
    
    # Start the bot! It will now listen for messages
    logger.info("Bot is now running and polling for messages!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# ============================================
# STEP 9: Actually start the bot when we run this file
# ============================================
if __name__ == '__main__':
    main()  # Call the main function to start everything!
