from telegram import Update
from telegram.ext import ContextTypes
from db import get_user
from handlers.levels import check_level_access
from config import LEVEL_ACADEMY, LEVEL_PROFILE

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    get_user(user_id)
    msg = "\u0633\u0644\u0627\u0645! \u0628\u0647 \u0631\u0628\u0627\u062a \u0647\u0627\u067e\u0648\u06cc\u06cc \u062e\u0648\u0634 \u0622\u0645\u062f\u06cc\u062f."
    await update.message.reply_text(msg)

async def academy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    if not check_level_access(user, LEVEL_ACADEMY):
        await update.message.reply_text("\u0634\u0645\u0627 \u0628\u0631\u0627\u06cc \u062f\u0633\u062a\u0631\u0633\u06cc \u0628\u0647 \u0622\u06a9\u0627\u062f\u0645\u06cc \u0646\u06cc\u0627\u0632 \u0628\u0647 \u0633\u0637\u062d \u0f11 \u062f\u0627\u0631\u06cc\u062f.")
        return
    text = (
        "\u0631\u0627\u0647\u0646\u0645\u0627\u06cc \u0622\u06a9\u0627\u062f\u0645\u06cc \u0647\u0627\u067e\u0648\u06cc\u06cc:\n"
        "- \u0647\u0627\u067e (Level 1)\n"
        "- \u0645\u0627\u0647\u06cc\u06af\u06cc\u0631\u06cc (Level 1)\n"
        "- \u0628\u0627\u0646\u06a9 (Level 2)\n"
        "- \u06a9\u0627\u0632\u06cc\u0646\u0648 (Level 3)\n"
        "- \u0627\u0646\u0628\u0627\u0631 \u0645\u0627\u0647\u06cc \u0648 \u0642\u0627\u062d\u0627\u0642 (Level 4)"
    )
    await update.message.reply_text(text)

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    if not check_level_access(user, LEVEL_PROFILE):
        await update.message.reply_text("\u0633\u0637\u062d \u0634\u0645\u0627 \u06a9\u0627\u0611\u06cc \u0646\u06cc\u0633\u062a.")
        return

    text = (
        f"\u067e\u0631\u0648\u0641\u0627\u06cc\u0644 \u0634\u0645\u0627:\n"
        f"\u0645\u0648\u062c\u0648\u062f\u06cc: {user['points']}\n"
        f"\u0633\u0637\u062d: {user['level']}\n"
        f"XP: {user['xp']}/35\n"
        f"\u0645\u0627\u0647\u06cc\u200c\u0647\u0627: {user['fish']}\n"
        f"\u0633\u06af\u200c\u0647\u0627: {user['dogs']}\n"
        f"\u0645\u0648\u062c\u0648\u062f\u06cc \u0628\u0627\u0646\u06a9: {user['bank_balance']}"
    )

    photos = await context.bot.get_user_profile_photos(user_id, limit=1)
    if photos.total_count > 0:
        file_id = photos.photos[0][-1].file_id
        await update.message.reply_photo(photo=file_id, caption=text)
    else:
        await update.message.reply_text(text)