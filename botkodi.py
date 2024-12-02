import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Salom! Men OpenAI yordamida javob beraman. Savol bering.')

# Botga xabar yuborish
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    bot_reply = chat_with_openai(user_message)
    update.message.reply_text(bot_reply)

# Botni ishga tushirish
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Komandalar
    dispatcher.add_handler(CommandHandler("start", start))

    # Xabarlarni ishlash
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Botni boshlash
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
