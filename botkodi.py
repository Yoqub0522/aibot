from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai
import os
from dotenv import load_dotenv

# .env faylidan kalitni yuklash
load_dotenv()

# OpenAI API kaliti
openai.api_key = os.getenv("OPENAI_API_KEY")

# Telegram bot tokeni
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# OpenAI bilan so'rov yuborish
def chat_with_openai(message_text):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # Yangi modelni tanlash
        messages=[{"role": "user", "content": message_text}],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()


# Botni boshlash
async def start(update, context):
    await update.message.reply_text('Salom! Men OpenAI yordamida javob beraman. Savol bering.')

# Botga xabar yuborish
async def handle_message(update, context):
    user_message = update.message.text
    bot_reply = chat_with_openai(user_message)
    await update.message.reply_text(bot_reply)

def main():
    # Application ob'ektini yaratish
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Komandalar
    application.add_handler(CommandHandler("start", start))

    # Xabarlarni ishlash
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Pollingni ishlatish
    application.run_polling()

if __name__ == '__main__':
    main()
