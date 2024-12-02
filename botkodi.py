import openai
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# OpenAI API kaliti
openai.api_key = 'sk-svcacct-CndFXdkK-T2ZpdszKqvFchzC-U2TokrbmHcojRZBHkZgNTUGnBTVjUWdLjkjQkLUT3BlbkFJsn0V3cPzlUMhmVITJfv0pMNc2w2hXV72pVbWT3Dyu8gh75LtPlmEP9A_oZEA_vkA'

# Telegram bot tokeni
TELEGRAM_TOKEN = '8178082976:AAGzrbAKLoCYDQmS-nPhm_BE5BlDxzb2TpI'

# OpenAI bilan so'rov yuborish
def chat_with_openai(message_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message_text,
        max_tokens=150
    )
    return response.choices[0].text.strip()

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

    # Agar webhook ishlatmoqchi bo'lsangiz:
    port = int(os.getenv('PORT', 5000))  # Portni atrof-muhitdan olish
    application.run_webhook(listen="0.0.0.0", port=port, url_path=TELEGRAM_TOKEN)  # Webhookni sozlash

    # Pollingni ishlatishda portni belgilash zarur emas
    application.run_polling()

if __name__ == '__main__':
    main()
