import os
import openai
import requests
import json
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# OpenAI API key and Telegram API token
openai.api_key = os.getenv('sk-svcacct-CndFXdkK-T2ZpdszKqvFchzC-U2TokrbmHcojRZBHkZgNTUGnBTVjUWdLjkjQkLUT3BlbkFJsn0V3cPzlUMhmVITJfv0pMNc2w2hXV72pVbWT3Dyu8gh75LtPlmEP9A_oZEA_vkA')
TELEGRAM_API_TOKEN = os.getenv('7761761615:AAGsS0KKBO8T-MVBsfsHHHMC6BMoqY4OTts')

if TELEGRAM_API_TOKEN is None:
    raise ValueError("Telegram API token is not set!")

# Flask app initialization
app = Flask(__name__)

# Telegram bot application object
application = None  # Global variable to hold the application object

# Flask routes
@app.route('/')
def home():
    return "Salom! Flask serveri ishlamoqda."

# OpenAI API interaction
def generate_openai_response(prompt: str) -> str:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # or another model you prefer
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

# Handle messages from users on Telegram
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # User's message
    print(f"Foydalanuvchidan xabar: {user_message}")
    
    # Get response from OpenAI
    openai_response = generate_openai_response(user_message)
    
    # Send OpenAI response back to the user
    await update.message.reply_text(openai_response)

# /start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Salom! Men OpenAI yordamida ishlovchi botman. Savollarni berishingiz mumkin.")

# Set webhook for Telegram
def set_webhook():
    WEBHOOK_URL = f'https://your-flask-server-url.com/{TELEGRAM_API_TOKEN}'
    set_webhook_url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook?url={WEBHOOK_URL}'
    response = requests.get(set_webhook_url)
    print(f"Webhook sozlash javobi: {response.text}")  # Check response from Telegram

# Webhook route to handle incoming updates
@app.route(f'/{TELEGRAM_API_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')  # Get JSON data from the request
    update = Update.de_json(json.loads(json_str), None)  # Convert JSON to Python object
    if application:
        application.process_update(update)  # Process the update with Telegram application
    return 'OK', 200

def main():
    global application  # Declare global variable
    # Initialize the Telegram application
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Set webhook
    set_webhook()

if __name__ == '__main__':
    # Start the Flask app and set up the Telegram bot
    main()

    # Run the Flask server
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 10000)))
