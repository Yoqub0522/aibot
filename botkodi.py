import asyncio
from flask import Flask
from telegram import Bot
from telegram.ext import Application, CommandHandler

app = Flask(__name__)

async def start(update, context):
    await update.message.reply_text('Salom!')

async def main():
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    application.add_handler(CommandHandler("start", start))

    # Botni fon ishida ishlatish
    await application.run_polling()

@app.route('/')
def hello_world():
    return "Salom, dunyo!"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # Botni fon ishida ishga tushiring
    app.run(host='0.0.0.0', port=8080)
