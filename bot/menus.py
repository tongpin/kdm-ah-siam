from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from config.settings import ADMIN_IDS, MINI_APP_URL
from storage.wiki_storage import load_wiki

def is_admin(user_id): return int(user_id) in ADMIN_IDS

def main_menu(user_id):
    keyboard = [[InlineKeyboardButton("📱 Open Minecraft Guide App", web_app=WebAppInfo(url=MINI_APP_URL))], [InlineKeyboardButton("🔎 Search", callback_data="search")]]
    row=[]
    for slug, lesson in list(load_wiki().items())[:8]:
        row.append(InlineKeyboardButton(lesson.get("title", slug)[:24], callback_data=f"lesson:{slug}"))
        if len(row)==2:
            keyboard.append(row); row=[]
    if row: keyboard.append(row)
    if is_admin(user_id): keyboard.append([InlineKeyboardButton("⚙️ Admin", callback_data="admin")])
    return InlineKeyboardMarkup(keyboard)

def admin_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("➕ Add Lesson", callback_data="admin:add")], [InlineKeyboardButton("📚 List Lessons", callback_data="admin:list")], [InlineKeyboardButton("🗑 Delete Lesson", callback_data="admin:delete")], [InlineKeyboardButton("🔙 Main Menu", callback_data="menu")]])

def back_menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menu", callback_data="menu")]])
