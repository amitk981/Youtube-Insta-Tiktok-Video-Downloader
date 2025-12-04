import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MONETAG_LINK = "https://otieu.com/4/10256428"

def handler(event, context):
    """Netlify function handler"""
    print(f"Received request: {event.get('httpMethod', 'UNKNOWN')}")
    
    # Health check
    if event.get('httpMethod') == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'Bot is running', 'token_set': bool(TOKEN)})
        }
    
    # Webhook handler
    if event.get('httpMethod') == 'POST':
        try:
            if not TOKEN:
                print("ERROR: TELEGRAM_BOT_TOKEN not set")
                return {'statusCode': 500, 'body': 'Token missing'}
            
            # Parse update
            body = json.loads(event.get('body', '{}'))
            print(f"Received update: {json.dumps(body)[:200]}")
            
            # Handle /start command
            if 'message' in body and 'text' in body['message']:
                if body['message']['text'] == '/start':
                    chat_id = body['message']['chat']['id']
                    
                    # Send monetag link
                    import requests
                    keyboard = {
                        'inline_keyboard': [[
                            {'text': '🎁 Click here to access bot', 'url': MONETAG_LINK}
                        ]]
                    }
                    
                    response = requests.post(
                        f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                        json={
                            'chat_id': chat_id,
                            'text': '🎬 Welcome to Video Downloader Bot!\n\nTo use this bot, please verify you are human by clicking the link below:',
                            'reply_markup': keyboard
                        }
                    )
                    print(f"Sent message, status: {response.status_code}")
            
            return {'statusCode': 200, 'body': 'OK'}
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'statusCode': 500, 'body': str(e)}
    
    return {'statusCode': 405, 'body': 'Method not allowed'}
