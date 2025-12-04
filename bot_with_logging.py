import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure detailed logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = "8230083195:AAFSxwz5tyDx5VTPaJ2aURk4zy1P3a6ONNY"
MONETAG_LINK = "https://otieu.com/4/10256428"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with Monetag link"""
    logger.info(f"User {update.effective_user.id} started the bot")
    
    keyboard = [
        [InlineKeyboardButton("🎁 Click here to access bot", url=MONETAG_LINK)],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎬 Welcome to Video Downloader Bot!\n\n"
        "To use this bot, please verify you are human by clicking the link below:",
        reply_markup=reply_markup
    )
    logger.info(f"Sent monetag link to user {update.effective_user.id}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    logger.info(f"User {update.effective_user.id} requested help")
    await update.message.reply_text(
        "📖 How to use:\n"
        "1. Click the verification link\n"
        "2. Send me a YouTube, TikTok, or Instagram link\n"
        "3. I'll download and send you the video!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    logger.info(f"User {user_id} sent message: {message_text}")
    
    await update.message.reply_text(
        "✅ Message received!\n"
        f"You sent: {message_text}\n\n"
        "Note: Download functionality is currently disabled for testing."
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)

def main():
    """Start the bot"""
    logger.info("Starting bot with logging enabled...")
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start polling
    logger.info("Bot is now running. Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
