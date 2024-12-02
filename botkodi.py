import openai
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask, request

# .env faylini yuklash
load_dotenv()

# OpenAI API kaliti
openai.api_key = os.getenv("OPENAI_API_KEY")

# Telegram bot tokeni
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Webhook URL
WEBHOOK_URL = os.getenv("https://aibot-9htc.onrender.com")  # Render platformasi uchun https://aibot-9htc.onrender.com kabi URL

# OpenAI bilan so'rov yuborish
def chat_with_openai(message_text):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # Yangi modelni tanlash
        messages=[{"role": "user", "content": message_text}],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

# Flask web-serverni yaratish
app = Flask(__name__)

# Botni boshlash
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Salom! Men OpenAI yordamida javob beraman. Savol bering.')

# Botga xabar yuborish
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    bot_reply = chat_with_openai(user_message)
    await update.message.reply_text(bot_reply)

# Webhook orqali Telegramdan xabar qabul qilish
@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, application.bot)
    application.process_update(update)
    return 'OK', 200

# Botni ishga tushirish
def main():
    # Application ob'ektini yaratish
    global application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Komandalar
    application.add_handler(CommandHandler("start", start))

    # Xabarlarni ishlash
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Webhookni sozlash va botni boshlash
    application.bot.set_webhook(url=WEBHOOK_URL + f'/{TELEGRAM_TOKEN}')

    # Flaskni ishga tushurish (Render platformasida)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

if __name__ == '__main__':
    main()
