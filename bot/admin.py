from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from bot.menus import is_admin, main_menu
from storage.wiki_storage import load_wiki, save_wiki

# States
ASK_SLUG, ASK_TITLE, ASK_CATEGORY, ASK_TEXT, ASK_KEYWORDS, ASK_ALIASES, ASK_IMAGES, ASK_VIDEOS = range(8)


# Start adding lesson
async def start_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.edit_message_text("⛔ Admin only.")
        return ConversationHandler.END

    await query.edit_message_text(
        "➕ Lesson slug?\n\nExample:\njava\nbedrock\nport-forward"
    )
    return ASK_SLUG


async def ask_slug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["slug"] = update.message.text.lower().strip().replace(" ", "-")
    await update.message.reply_text("Title?\nExample: ☕ Java Server Setup")
    return ASK_TITLE


async def ask_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text.strip()
    await update.message.reply_text("Category?\nExample: setup / network / plugins")
    return ASK_CATEGORY


async def ask_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["category"] = update.message.text.lower().strip()
    await update.message.reply_text("Lesson text?")
    return ASK_TEXT


async def ask_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["text"] = update.message.text.strip()
    await update.message.reply_text(
        "Keywords? (comma separated)\nExample: java, server, setup"
    )
    return ASK_KEYWORDS


async def ask_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["keywords"] = [
        x.strip().lower()
        for x in update.message.text.split(",")
        if x.strip()
    ]
    await update.message.reply_text(
        "Aliases? (comma separated)\nExample: how to setup server, jar file"
    )
    return ASK_ALIASES


async def ask_aliases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["aliases"] = [
        x.strip().lower()
        for x in update.message.text.split(",")
        if x.strip()
    ]
    await update.message.reply_text(
        "Image URLs? (comma separated) or type skip"
    )
    return ASK_IMAGES


async def ask_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.lower() == "skip":
        context.user_data["images"] = []
    else:
        context.user_data["images"] = [
            x.strip() for x in text.split(",") if x.strip()
        ]

    await update.message.reply_text(
        "Video URLs? (comma separated) or type skip"
    )
    return ASK_VIDEOS


async def ask_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.lower() == "skip":
        videos = []
    else:
        videos = [x.strip() for x in text.split(",") if x.strip()]

    slug = context.user_data["slug"]

    wiki = load_wiki()

    wiki[slug] = {
        "title": context.user_data["title"],
        "category": context.user_data["category"],
        "text": context.user_data["text"],
        "keywords": context.user_data["keywords"],
        "aliases": context.user_data["aliases"],
        "images": context.user_data["images"],
        "videos": videos,
    }

    save_wiki(wiki)
    context.user_data.clear()

    await update.message.reply_text(
        f"✅ Lesson saved: {slug}",
        reply_markup=main_menu(update.effective_user.id),
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Cancelled",
        reply_markup=main_menu(update.effective_user.id),
    )
    return ConversationHandler.END


# IMPORTANT: This must exist (your error was here before)
add_lesson_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_add, pattern="^admin:add$")
    ],
    states={
        ASK_SLUG: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_slug)],
        ASK_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_title)],
        ASK_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_category)],
        ASK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_text)],
        ASK_KEYWORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_keywords)],
        ASK_ALIASES: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_aliases)],
        ASK_IMAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_images)],
        ASK_VIDEOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_videos)],
    },
    fallbacks=[
        MessageHandler(filters.Regex("^/cancel$"), cancel)
    ],
)
