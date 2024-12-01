from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask
import logging

# Flask ilovasini yaratish
app = Flask(__name__)

@app.route('/healthz')
def health_check():
    return "OK", 200

# Telegram bot uchun logging sozlamalari
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Start komandasi
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Salom! Men sizning Telegram botingizman.')

# Main function for running the bot
async def main() -> None:
    application = Application.builder().token('your_telegram_token').build()
    
    # CommandHandler va MessageHandler ni qo'shish
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT, start))  # Bu yerda xohlagan komandalarni qo'shishingiz mumkin

    # Flask serverini alohida ipdan ishga tushurish
    from threading import Thread
    def run_flask():
        app.run(host='0.0.0.0', port=8080)

    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Telegram botni ishga tushurish
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
