import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.getenv("PORT", 5000))  # Render automatically provides a PORT environment variable

# Function for OpenAI communication
async def chat_with_openai(message_text):
    response = await openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message_text}],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Hello! I am your OpenAI assistant.')

# Handle incoming messages
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    bot_reply = await chat_with_openai(user_message)
    await update.message.reply_text(bot_reply)

async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Running the bot on the specified port for Render
    await application.run_webhook(
        listen="0.0.0.0",  # Listen on all IP addresses
        port=PORT,          # Use the port Render provides
        url_path=TELEGRAM_TOKEN
    )

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
