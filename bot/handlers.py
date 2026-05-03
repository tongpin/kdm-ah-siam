from telegram import Update
from telegram.ext import ContextTypes

from bot.menus import main_menu, admin_menu, back_menu, is_admin
from storage.wiki_storage import load_wiki, save_wiki, search_wiki

search_mode = set()
delete_mode = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    await update.message.reply_text(
        text=(
            "⛏️ <b>Minecraft Khmer Helper</b>\n\n"
            "📚 មេរៀន Minecraft Server ជាភាសាខ្មែរ\n"
            "🔎 Search guides or open the Mini App below.\n\n"
            "👇 ជ្រើសរើសមុខងារ:"
        ),
        parse_mode="HTML",
        reply_markup=main_menu(user_id)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if data == "menu":
        await query.edit_message_text(
            text=(
                "⛏️ <b>Minecraft Khmer Helper</b>\n\n"
                "📚 មេរៀន Minecraft Server ជាភាសាខ្មែរ\n"
                "👇 ជ្រើសរើសមុខងារ:"
            ),
            parse_mode="HTML",
            reply_markup=main_menu(user_id)
        )
        return

    if data == "search":
        search_mode.add(user_id)
        await query.edit_message_text(
            text="🔎 សូមវាយពាក្យស្វែងរក:"
        )
        return

    if data == "admin":
        if not is_admin(user_id):
            await query.edit_message_text("⛔ Admin only.")
            return

        await query.edit_message_text(
            text="⚙️ Admin Menu",
            reply_markup=admin_menu()
        )
        return

    if data == "admin:list":
        if not is_admin(user_id):
            await query.edit_message_text("⛔ Admin only.")
            return

        wiki = load_wiki()

        if not wiki:
            text = "📚 No lessons yet."
        else:
            text = "📚 Lessons:\n" + "\n".join(
                [
                    f"- {slug}: {lesson.get('title', slug)}"
                    for slug, lesson in wiki.items()
                ]
            )

        await query.edit_message_text(
            text=text,
            reply_markup=admin_menu()
        )
        return

    if data == "admin:delete":
        if not is_admin(user_id):
            await query.edit_message_text("⛔ Admin only.")
            return

        delete_mode.add(user_id)
        await query.edit_message_text(
            text=(
                "🗑 Type lesson slug to delete.\n\n"
                "Example:\n"
                "java"
            )
        )
        return

    if data.startswith("lesson:"):
        slug = data.split(":", 1)[1]
        wiki = load_wiki()
        lesson = wiki.get(slug)

        if not lesson:
            await query.edit_message_text(
                text="❌ Lesson not found.",
                reply_markup=back_menu()
            )
            return

        await query.edit_message_text(
            text=(
                f"{lesson.get('title', slug)}\n\n"
                f"{lesson.get('text', '')}"
            ),
            reply_markup=back_menu()
        )
        return

    await query.edit_message_text(
        text="❌ Unknown action.",
        reply_markup=back_menu()
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id in delete_mode:
        delete_mode.remove(user_id)

        if not is_admin(user_id):
            await update.message.reply_text("⛔ Admin only.")
            return

        slug = text.lower().replace(" ", "-")
        wiki = load_wiki()

        if slug in wiki:
            del wiki[slug]
            save_wiki(wiki)

            await update.message.reply_text(
                text="✅ Deleted lesson: {slug}",
                reply_markup=main_menu(user_id)
            )
        else:
            await update.message.reply_text(
                text="❌ Lesson not found.",
                reply_markup=main_menu(user_id)
            )

        return

    if user_id in search_mode:
        search_mode.remove(user_id)

        results = search_wiki(text)

        if not results:
            await update.message.reply_text(
                text="❌ រកមិនឃើញទេ។",
                reply_markup=main_menu(user_id)
            )
            return

        messages = []

        for item in results[:5]:
            title = item.get("title", item.get("slug", "Lesson"))
            lesson_text = item.get("text", "")

            messages.append(
                f"{title}\n\n{lesson_text[:700]}"
            )

        await update.message.reply_text(
            text="\n\n---\n\n".join(messages),
            reply_markup=main_menu(user_id)
        )
        return
