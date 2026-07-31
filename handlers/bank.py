from telegram import Update
from telegram.ext import ContextTypes
from db import get_user
from handlers.levels import check_level_access
from config import LEVEL_BANK

async def bank_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    if not check_level_access(user, LEVEL_BANK):
        await update.message.reply_text("\u0628\u0627\u0646\u06a9 \u0627\u0632 \u0633\u0637\u062d \u06f2 \u0628\u0627\u0632 \u0645\u06cc\u200c\u0634\u0648\u062f.")
        return
    await update.message.reply_text(f"\u0645\u0648\u062c\u0648\u062f\u06cc \u0628\u0627\u0646\u06a9: {user['bank_balance']}")