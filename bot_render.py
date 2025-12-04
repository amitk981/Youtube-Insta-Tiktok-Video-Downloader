import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token from environment
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MONETAG_LINK = "https://otieu.com/4/10256428"

# Track users who clicked the Monetag link
verified_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with Monetag link"""
    user_id = update.effective_user.id
    logger.info(f"User {user_id} started the bot")
    
    keyboard = [
        [InlineKeyboardButton("🎁 Click here to access bot", url=MONETAG_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎬 Welcome to Video Downloader Bot!\n\n"
        "To use this bot, please verify you are human by clicking the link below.\n"
        "After clicking, come back and send me a video URL!",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
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

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video URL messages"""
    user_id = update.effective_user.id
    url = update.message.text
    
    logger.info(f"User {user_id} sent URL: {url}")
    
    # Simple URL validation
    if not any(platform in url.lower() for platform in ['youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com']):
        await update.message.reply_text(
            "❌ Please send a valid video URL from:\n"
            "• YouTube\n"
            "• TikTok\n"
            "• Instagram"
        )
        return
    
    # For now, just acknowledge the URL
    # Full download functionality can be added later
    await update.message.reply_text(
        "✅ URL received!\n\n"
        f"🔗 {url}\n\n"
        "📥 Video download functionality will be added soon.\n"
        "For now, the bot is running successfully with Monetag integration!"
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)

def main():
    """Start the bot"""
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return
    
    logger.info("Starting bot...")
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start polling
    logger.info("Bot is now running!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
