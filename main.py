import threading

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config.settings import TELEGRAM_TOKEN, WEB_HOST, WEB_PORT
from bot.handlers import start, button, handle_text
from bot.admin import add_lesson_handler
from web.api import app as flask_app


def run_web():
    print(f"🌐 API running on {WEB_HOST}:{WEB_PORT}")
    flask_app.run(
        host=WEB_HOST,
        port=WEB_PORT,
        debug=False,
        use_reloader=False,
    )


def run_bot():
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "PUT_YOUR_NEW_BOT_TOKEN_HERE":
        raise RuntimeError(
            "❌ TELEGRAM_TOKEN is missing. Set it in config.yml or environment variables."
        )

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Important: add conversation handler before general callback handler
    app.add_handler(add_lesson_handler)

    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Telegram bot running...")
    app.run_polling()


if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()

    run_bot()
