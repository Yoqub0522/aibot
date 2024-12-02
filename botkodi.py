import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai
from dotenv import load_dotenv

# Muhit o'zgaruvchilarini yuklash
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 5000))  # Render uchun port

# OpenAI API kalitini sozlash
openai.api_key = OPENAI_API_KEY

# OpenAI bilan muloqot qilish funksiyasi
async def chat_with_openai(message_text):
    # Asynchronous OpenAI API calls via to_thread
    response = await asyncio.to_thread(openai.ChatCompletion.create,
                                        model="gpt-3.5-turbo",
                                        messages=[{"role": "user", "content": message_text}],
                                        max_tokens=150)
    return response['choices'][0]['message']['content'].strip()

# /start komandasi uchun handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Assalomu alaykum! Men OpenAI yordamchingizman.')

# Foydalanuvchi xabarlarini qayta ishlash
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    bot_reply = await chat_with_openai(user_message)
    await update.message.reply_text(bot_reply)

# Botni ishga tushirish
async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlerlarni qo‘shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Render uchun webhook sozlash
    webhook_url = f"https://<SIZNING_DOMAIN>/{TELEGRAM_TOKEN}"  # <SIZNING_DOMAIN> ni o'zgartiring
    await application.run_webhook(
        listen="0.0.0.0",  # Barcha IP-manzillardan tinglash
        port=PORT,         # Render bergan port
        url_path=TELEGRAM_TOKEN,
        webhook_url=webhook_url
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"Xatolik: {e}")
