import os
import openai
from dotenv import load_dotenv
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import json
import asyncio

# Load environment variables from the .env file (if running locally)
load_dotenv()

# Retrieve the API tokens from environment variables
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Ensure the environment variables are set
if TELEGRAM_API_TOKEN is None:
    raise ValueError("Telegram API token is not set!")
if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key is not set!")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram application
application = None  # Will be set in the main function

# Flask endpoint to check if the server is running
@app.route('/')
def home():
    return "Salom! Flask serveri ishlamoqda."

# Function to generate a response from OpenAI's API
def generate_openai_response(prompt: str) -> str:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use other models like 'gpt-3.5-turbo' if needed
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

# Handler to process incoming messages from Telegram users
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # User's message
    print(f"Foydalanuvchidan xabar: {user_message}")
    
    # Get response from OpenAI
    openai_response = generate_openai_response(user_message)
    
    # Send OpenAI response to the user
    await update.message.reply_text(openai_response)

# Command handler for the /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Salom! Men OpenAI yordamida ishlovchi botman. Savollarni berishingiz mumkin.")

# Function to set up the webhook for Telegram
def set_webhook():
    # Replace with your actual Flask app URL from ngrok or your hosted app
    WEBHOOK_URL = f'https://your-ngrok-url.ngrok.io/{TELEGRAM_API_TOKEN}'  # Example using ngrok URL
    set_webhook_url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/setWebhook?url={WEBHOOK_URL}'
    response = requests.get(set_webhook_url)
    print(f"Webhook sozlash javobi: {response.text}")  # Response from the setWebhook call

# Webhook endpoint for handling Telegram updates
@app.route(f'/{TELEGRAM_API_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')  # Incoming JSON data
    update = Update.de_json(json.loads(json_str), None)  # Convert JSON to Python object
    if application:
        asyncio.run(application.process_update(update))  # Process the update with the Telegram bot application
    return 'OK', 200

# Main function to set up the Telegram bot and Flask app
def main():
    global application  # Declare as global to use in other parts of the code

    # Create the Telegram application
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Add handlers for Telegram commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Set up the webhook
    set_webhook()

# Run the Flask and Telegram bot
if __name__ == '__main__':
    # Run the bot setup
    main()

    # Start the Flask server
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 8080)))  # Default to port 10000 if not set
