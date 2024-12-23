import os
from dotenv import load_dotenv
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import json
import asyncio

# Load environment variables
load_dotenv()

# Retrieve API tokens
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
GEMINI_AI_KEY = os.getenv('GEMINI_AI_KEY', 'AIzaSyDU7-n3OXubckqG2DEzz9LLSelzTtmpHoY')

if not TELEGRAM_API_TOKEN:
    raise ValueError("Telegram API token is not set!")
if not GEMINI_AI_KEY:
    raise ValueError("Gemini AI key is not set!")

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask health check endpoint
@app.route('/')
def home():
    return "Salom! Flask serveri ishlamoqda."

# Generate a response from Gemini AI
def generate_gemini_response(prompt: str) -> str:
    try:
        url = "https://gemini-api-endpoint.example.com/v1/completions"  # Replace with the correct endpoint
        headers = {
            "Authorization": f"Bearer {GEMINI_AI_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "maxTokens": 150
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()
        return data.get("choices", [{}])[0].get("text", "Javobni olishda xatolik yuz berdi.")
    except Exception as e:
        logger.error(f"Error generating Gemini response: {e}")
        return "Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."

# Telegram message handler
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")
    gemini_response = generate_gemini_response(user_message)
    await update.message.reply_text(gemini_response)

# Telegram /start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Salom! Men Gemini AI yordamida ishlovchi botman. Savollarni berishingiz mumkin.")

# Set up Telegram webhook
def set_webhook():
    ngrok_url = os.getenv('NGROK_URL')
    if not ngrok_url:
        raise ValueError("NGROK_URL environment variable is not set!")

    webhook_url = f'{ngrok_url}/{TELEGRAM_API_TOKEN}'
    set_webhook_url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook?url={webhook_url}'
    
    response = requests.get(set_webhook_url)
    logger.info(f"Webhook setup response: {response.text}")

# Telegram webhook endpoint
@app.route(f'/{TELEGRAM_API_TOKEN}', methods=['POST'])
def webhook():
    try:
        json_str = request.get_data().decode('UTF-8')
        update = Update.de_json(json.loads(json_str), None)
        if application:
            asyncio.run(application.process_update(update))
        return 'OK', 200
    except Exception as e:
        logger.error(f"Error processing webhook update: {e}")
        return 'Error', 500

# Main function
def main():
    global application
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    set_webhook()

if __name__ == '__main__':
    main()
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 8080)))
