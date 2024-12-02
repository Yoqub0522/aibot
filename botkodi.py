import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# .env faylini yuklash
load_dotenv()

# OpenAI API kaliti
openai.api_key = os.getenv("OPENAI_API_KEY")

# Telegram bot tokeni
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Webhook URL
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not WEBHOOK_URL or not TELEGRAM_TOKEN:
    raise ValueError("WEBHOOK_URL or TELEGRAM_TOKEN is missing")

# OpenAI bilan so'rov yuborish
def chat_with_openai(message_text):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # Yangi modelni tanlash
        messages=[{"role": "user", "content": message_text}],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

# Botni boshlash
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Salom! Men OpenAI yordamida javob beraman. Savol bering.')

# Botga xabar yuborish
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    bot_reply = chat_with_openai(user_message)
    await update.message.reply_text(bot_reply)

# Botni ishga tushirish
def main():
    # Application ob'ektini yaratish
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Komandalar
    application.add_handler(CommandHandler("start", start))

    # Xabarlarni ishlash
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Webhookni sozlash va botni boshlash
    application.bot.set_webhook(url=WEBHOOK_URL + f'/{TELEGRAM_TOKEN}')

    # Portni olish (Render platformasida kerakli portni o'rnatish)
    port = int(os.getenv("PORT", 5000))  # Agar PORT o'zgaruvchisi mavjud bo'lmasa, 5000 port ishlatiladi

    # Webhookni sozlash va botni boshlash
    application.run_webhook(
        listen="0.0.0.0",  # Botni barcha IP manzillardan eshitish
        port=port,         # Portni sozlash
        url_path=TELEGRAM_TOKEN  # Webhook uchun URL yo'lini sozlash
    )

if __name__ == '__main__':
    main()
