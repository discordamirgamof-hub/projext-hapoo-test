import random
from telegram import Update
from telegram.ext import ContextTypes
from db import get_user, update_user, add_xp
from handlers.levels import check_level_access, is_in_prison
from config import LEVEL_HAP, HAP_XP_REWARD

async def hap_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not check_level_access(user, LEVEL_HAP):
        await update.message.reply_text("\u0633\u0637\u062d \u0634\u0645\u0627 \u06a9\u0627\u0611\u06cc \u0646\u06cc\u0633\u062a.")
        return

    if is_in_prison(user):
        await update.message.reply_text("\u0634\u0645\u0627 \u062f\u0631 \u0632\u0646\u062f\u0627\u0646 \u0647\u0633\u062a\u06cc\u062f \u0648 \u0646\u0645\u06cc\200c\u062a\u0648\u0627\u0646\u06cc\u062f \u0641\u0639\u0627\u0644\u06cc\u062a \u06a9\u0646\u06cc\u062f.")
        return

    reward = random.randint(10, 90)
    update_user(user_id, points=user["points"] + reward)
    add_xp(user_id, HAP_XP_REWARD)
    await update.message.reply_text(f"\u0634\u0645\u0627 {reward} \u067e\u0648\u06cc\u0646\u062a \u0648 {HAP_XP_REWARD} XP \u062f\u0631\u06cc\u0627\u0641\u062a \u06a9\u0631\u062f\u06cc\u062f!")