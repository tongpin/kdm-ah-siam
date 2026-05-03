import threading
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config.settings import TELEGRAM_TOKEN, WEB_HOST, WEB_PORT
from bot.handlers import start, button, handle_text
from bot.admin import add_lesson_handler
from web.api import app as flask_app

def run_web(): flask_app.run(host=WEB_HOST, port=WEB_PORT)
def run_bot():
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == 'PUT_YOUR_NEW_BOT_TOKEN_HERE': raise RuntimeError('Set your TELEGRAM_TOKEN in config.yml or environment variables first.')
    app=Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start)); app.add_handler(add_lesson_handler); app.add_handler(CallbackQueryHandler(button)); app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print('Telegram bot running...'); app.run_polling()
if __name__=='__main__':
    threading.Thread(target=run_web, daemon=True).start(); print(f'API running on {WEB_HOST}:{WEB_PORT}'); run_bot()
