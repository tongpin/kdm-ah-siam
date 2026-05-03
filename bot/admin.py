from telegram import Update
from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from bot.menus import is_admin, main_menu
from storage.wiki_storage import load_wiki, save_wiki
ASK_SLUG, ASK_TITLE, ASK_CATEGORY, ASK_TEXT, ASK_KEYWORDS, ASK_ALIASES, ASK_IMAGES, ASK_VIDEOS = range(8)

async def start_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer()
    if not is_admin(q.from_user.id): await q.edit_message_text("⛔ Admin only."); return ConversationHandler.END
    await q.edit_message_text("➕ Lesson slug?
Example: java, bedrock, port-forward"); return ASK_SLUG
async def ask_slug(update, context): context.user_data['slug']=update.message.text.lower().strip().replace(' ','-'); await update.message.reply_text('Title?
Example: ☕ Java Server Setup'); return ASK_TITLE
async def ask_title(update, context): context.user_data['title']=update.message.text.strip(); await update.message.reply_text('Category?
Example: setup, network, plugins'); return ASK_CATEGORY
async def ask_category(update, context): context.user_data['category']=update.message.text.lower().strip(); await update.message.reply_text('Lesson text?'); return ASK_TEXT
async def ask_text(update, context): context.user_data['text']=update.message.text.strip(); await update.message.reply_text('Keywords? Use comma.
Example: java, server, setup, eula'); return ASK_KEYWORDS
async def ask_keywords(update, context): context.user_data['keywords']=[x.strip().lower() for x in update.message.text.split(',') if x.strip()]; await update.message.reply_text('Aliases? Use comma.
Example: how to setup server, jar file, បង្កើត server'); return ASK_ALIASES
async def ask_aliases(update, context): context.user_data['aliases']=[x.strip().lower() for x in update.message.text.split(',') if x.strip()]; await update.message.reply_text('Image URLs? Use comma or type skip'); return ASK_IMAGES
async def ask_images(update, context):
    raw=update.message.text.strip(); context.user_data['images']=[] if raw.lower()=='skip' else [x.strip() for x in raw.split(',') if x.strip()]
    await update.message.reply_text('Video URLs? Use comma or type skip'); return ASK_VIDEOS
async def ask_videos(update, context):
    raw=update.message.text.strip(); videos=[] if raw.lower()=='skip' else [x.strip() for x in raw.split(',') if x.strip()]
    wiki=load_wiki(); slug=context.user_data['slug']
    wiki[slug]={'title':context.user_data['title'],'category':context.user_data['category'],'text':context.user_data['text'],'keywords':context.user_data['keywords'],'aliases':context.user_data['aliases'],'images':context.user_data['images'],'videos':videos}
    save_wiki(wiki)
    await update.message.reply_text(f'✅ Lesson saved: {slug}

Mini App will show it if API URL is connected.', reply_markup=main_menu(update.effective_user.id)); return ConversationHandler.END
add_lesson_handler = ConversationHandler(entry_points=[CallbackQueryHandler(start_add, pattern='^admin:add$')], states={ASK_SLUG:[MessageHandler(filters.TEXT & ~filters.COMMAND, ask_slug)],ASK_TITLE:[MessageHandler(filters.TEXT & ~filters.COMMAND, ask_title)],ASK_CATEGORY:[MessageHandler(filters.TEXT & ~filters.COMMAND, ask_category)],ASK_TEXT:[MessageHandler(filters.TEXT & ~filters.COMMAND, ask_text)],ASK_KEYWORDS:[MessageHandler(filters.TEXT & ~filters.COMMAND, ask_keywords)],ASK_ALIASES:[MessageHandler(filters.TEXT & ~filters.COMMAND, ask_aliases)],ASK_IMAGES:[MessageHandler(filters.TEXT & ~filters.COMMAND, ask_images)],ASK_VIDEOS:[MessageHandler(filters.TEXT & ~filters.COMMAND, ask_videos)]}, fallbacks=[])
