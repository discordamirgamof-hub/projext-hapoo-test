import random
from telegram import Update
from telegram.ext import ContextTypes
from db import get_user, update_user, add_xp
from handlers.levels import check_level_access, is_in_prison
from config import LEVEL_FISHING, LEVEL_SELL_FISH, LEVEL_INVENTORY, FISHING_XP_REWARD

async def fishing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if not check_level_access(user, LEVEL_FISHING):
        await update.message.reply_text("\u0633\u0637\u062d \u0634\u0645\u0627 \u06a9\u0627\u0611\u06cc \u0646\u06cc\u0633\u062a.")
        return

    if is_in_prison(user):
        await update.message.reply_text("\u0634\u0645\u0627 \u062f\u0631 \u0632\u0646\u062f\u0627\u0646 \u0647\u0633\u062a\u06cc\u062f.")
        return

    caught = random.randint(1, 3)
    update_user(user_id, fish=user["fish"] + caught)
    add_xp(user_id, FISHING_XP_REWARD)
    await update.message.reply_text(f"\u0634\u0645\u0627 {caught} \u0645\u0627\u0647\u06cc \u06af\u0631\u0641\u062a\u06cc\u062f!")

async def sell_fish_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if not check_level_access(user, LEVEL_SELL_FISH):
        await update.message.reply_text("\u0633\u0637\u062d \u0634\u0645\u0627 \u06a9\u0627\u0611\u06cc \u0646\u06cc\u0633\u062a.")
        return

    if user["fish"] <= 0:
        await update.message.reply_text("\u0645\u0627\u0647\u06cc \u0628\u0631\u0627\u06cc \u0641\u0631\u0648\u0634 \u0646\u062f\u0627\u0631\u06cc\u062f.")
        return

    earnings = user["fish"] * 100
    update_user(user_id, points=user["points"] + earnings, fish=0)
    await update.message.reply_text(f"\u0645\u0627\u0647\u06cc\u200c\u0647\u0627 \u0628\u0647 \u0645\u0628\u0644\u063a {earnings} \u0641\u0631\u0648\u062e\u062a\u0647 \u0634\u062f\u0646\u062f.")

async def inventory_fish_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    if not check_level_access(user, LEVEL_INVENTORY):
        await update.message.reply_text("\u0627\u0646\u0628\u0627\u0631 \u0645\u0627\u0647\u06cc \u0627\u0632 \u0633\u0637\u062d \u06f4 \u0628\u0627\u0632 \u0645\u06cc\200c\u0634\u0648\u062f.")
        return

    await update.message.reply_text(f"\u062a\u0639\u062f\u0627\u062f \u0645\u0627\u0647\u06cc\u200c\u0647\u0627\u06cc \u0627\u0646\u0628\u0627\u0631: {user['fish']}")