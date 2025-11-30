import os
import json
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Retrieve token from Environment Variables (Setup in Phase 4)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Initialize App (Global to cache it for hot starts)
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # YOUR MONETAG STRATEGY:
    # Use an "Inline Keyboard" to make the ad look professional (like a button)
    monetag_link = "https://otieu.com/4/10256428" 
    
    keyboard = [
        [InlineKeyboardButton("🎁 Click here to access bot", url=monetag_link)],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome! To use this bot, please verify you are human by clicking the link below:",
        reply_markup=reply_markup
    )

async def process_update(event_body):
    # Hook the handlers
    if not application.handlers:
        application.add_handler(CommandHandler("start", start))

    # Process the update from Telegram
    await application.initialize()
    update = Update.de_json(json.loads(event_body), application.bot)
    await application.process_update(update)
    await application.shutdown()

def handler(event, context):
    # This is the entry point for Netlify
    if event['httpMethod'] == 'POST':
        asyncio.run(process_update(event['body']))
        return {'statusCode': 200, 'body': 'OK'}
    
    return {'statusCode': 200, 'body': 'Bot is running'}
