from telegram import Update
from telegram.ext import ContextTypes
from bot.menus import main_menu, admin_menu, back_menu, is_admin
from storage.wiki_storage import load_wiki, search_wiki, save_wiki
search_mode=set(); delete_mode=set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    await update.message.reply_text("⛏️ <b>Minecraft Khmer Helper</b>

📚 មេរៀន Minecraft Server ជាភាសាខ្មែរ
🔎 Search guides or open the Mini App below.", parse_mode="HTML", reply_markup=main_menu(uid))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query=update.callback_query; await query.answer(); uid=query.from_user.id; data=query.data
    if data=="menu":
        await query.edit_message_text("⛏️ <b>Minecraft Khmer Helper</b>

ជ្រើសរើសមុខងារ:", parse_mode="HTML", reply_markup=main_menu(uid)); return
    if data=="search":
        search_mode.add(uid); await query.edit_message_text("🔎 សូមវាយពាក្យស្វែងរក:"); return
    if data=="admin":
        if not is_admin(uid): await query.edit_message_text("⛔ Admin only."); return
        await query.edit_message_text("⚙️ Admin Menu", reply_markup=admin_menu()); return
    if data=="admin:list":
        wiki=load_wiki()
        text="📚 No lessons yet." if not wiki else "📚 Lessons:
" + "
".join([f"- {s}: {l.get('title',s)}" for s,l in wiki.items()])
        await query.edit_message_text(text, reply_markup=admin_menu()); return
    if data=="admin:delete":
        if not is_admin(uid): await query.edit_message_text("⛔ Admin only."); return
        delete_mode.add(uid); await query.edit_message_text("🗑 Type lesson slug to delete. Example: java"); return
    if data.startswith("lesson:"):
        slug=data.split(":",1)[1]; lesson=load_wiki().get(slug)
        if not lesson: await query.edit_message_text("❌ Lesson not found.", reply_markup=back_menu()); return
        await query.edit_message_text(f"{lesson.get('title',slug)}

{lesson.get('text','')}", reply_markup=back_menu()); return

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id; text=update.message.text.strip()
    if uid in delete_mode:
        delete_mode.remove(uid)
        if not is_admin(uid): await update.message.reply_text("⛔ Admin only."); return
        wiki=load_wiki(); slug=text.lower().replace(" ","-")
        if slug in wiki:
            del wiki[slug]; save_wiki(wiki); await update.message.reply_text(f"✅ Deleted: {slug}", reply_markup=main_menu(uid))
        else: await update.message.reply_text("❌ Not found.", reply_markup=main_menu(uid))
        return
    if uid not in search_mode: return
    search_mode.remove(uid); results=search_wiki(text)
    if not results: await update.message.reply_text("❌ រកមិនឃើញទេ។", reply_markup=main_menu(uid)); return
    msg=[]
    for item in results[:5]: msg.append(f"{item.get('title', item['slug'])}
{item.get('text','')[:400]}")
    await update.message.reply_text("

---

".join(msg), reply_markup=main_menu(uid))
