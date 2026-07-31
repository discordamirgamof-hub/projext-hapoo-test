import time
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db import get_user, update_user
from handlers.levels import check_level_access, is_in_prison
from config import LEVEL_SMUGGLE, DEFAULT_PRISON_FINE, PRISON_DURATION_SEC, ESCAPE_SUCCESS_RATE

async def smuggle_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if not check_level_access(user, LEVEL_SMUGGLE):
        await update.message.reply_text("\u0642\u0627\u062d\u0627\u0642 \u0633\u06af \u0627\u0632 \u0633\u0637\u062d \u06f4 \u0628\u0627\u0632 \u0645\u06cc\200c\u0634\u0648\u062f.")
        return

    if is_in_prison(user):
        await update.message.reply_text("\u0634\u0645\u0627 \u062f\u0631 \u0632\u0646\u062f\u0627\u0646 \u0647\u0633\u062a\u06cc\u062f.")
        return

    if user["dogs"] <= 3:
        await update.message.reply_text("\u0628\u0631\u0627\u06cc \u0642\u0627\u062d\u0627\u0642 \u0628\u0627\u06cc\u062f \u0628\u06cc\u0634 \u0627\u0632 \u06f3 \u0633\u06af \u062f\u0627\u0634\u062a\u0647 \u0628\u0627\u0634\u06cc\u062f.")
        return

    busted = random.choice([True, False])
    first_name = update.effective_user.first_name

    if busted:
        prison_until = int(time.time()) + PRISON_DURATION_SEC
        fine = DEFAULT_PRISON_FINE
        update_user(user_id, prison_until=prison_until, prison_fine=fine)

        text = (
            f"\u0622\u0642\u0627\u06cc {first_name} \u062e\u0648\u062f\u062a\u0648\u0646 \u0647\u0633\u062a\u06cc\u062f\u061f\u061f "
            f"\u0634\u0645\u0627 \u0628\u0647 \u062c\u0631\u0645 \u0642\u0627\u062d\u0627\u0642 \u0633\u06af\u200c\u0647\u0627\u06cc \u0628\u06cc\u200c\u06af\u0646\u0627\u0647 \u062e\u06cc\u0627\u0628\u0648\u0646\u06cc \u0628\u0647 \u06f1\u06f5 \u062f\u0642\u06cc\u0642\u0647 \u062d\u0628\u0633 \u0645\u062d\u06a9\u0648\u0645 \u0647\u0633\u062a\u06cc\u062f \u06cc\u0627 \u0627\u06cc\u0646\u06a9\u0647 \u062c\u0631\u06cc\u0645\u0647 \u062f\u0631 \u0635\u0648\u0631\u062a \u0641\u0631\u0627\u0631 \u062d\u06a9\u0645 \u062f\u0648 \u0628\u0631\u0627\u0628\u0631 \u0645\u06cc\200c\u0634\u0648\u062f."
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("\u0641\u0631\u0627\u0631 \u0627\u0632 \u0632\u0646\u062f\u0627\u0646", callback_data="escape_prison")],
            [InlineKeyboardButton(f"\u067e\u0631\u062f\u0627\u062e\u062a \u062c\u0631\u06cc\u0645\u0647 ({fine})", callback_data="pay_fine")]
        ])
        await update.message.reply_text(text, reply_markup=keyboard)
    else:
        reward = user["dogs"] * 500
        update_user(user_id, points=user["points"] + reward, dogs=0)
        await update.message.reply_text(f"\u0642\u0627\u062d\u0627\u0642 \u0645\u0648\u0641\u0642\u06cc\u062a\u200c\u0622\u0645\u06cc\u0632 \u0628\u0648\u062f! {reward} \u067e\u0648\u06cc\u0646\u062a \u06a9\u0633\u0628 \u06a9\u0631\u062f\u06cc\u062f.")

async def prison_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user = get_user(user_id)

    if query.data == "escape_prison":
        success = random.random() < ESCAPE_SUCCESS_RATE
        if success:
            update_user(user_id, prison_until=0, prison_fine=0)
            await query.edit_message_text("\u0634\u0645\u0627 \u0628\u0627 \u0645\u0648\u0641\u0642\u06cc\u062a \u0627\u0632 \u0632\u0646\u062f\u0627\u0646 \u0641\u0631\u0627\u0631 \u06a9\u0631\u062f\u06cc\u062f!")
        else:
            new_until = int(time.time()) + (PRISON_DURATION_SEC * 2)
            new_fine = user["prison_fine"] * 2
            update_user(user_id, prison_until=new_until, prison_fine=new_fine)
            await query.edit_message_text(f"\u0641\u0631\u0627\u0631 \u0646\u0627\u0645\u0648\u0641\u0642 \u0628\u0648\u062f! \u062d\u06a9\u0645 \u0634\u0645\u0627 \u06f3\u06f0 \u062f\u0642\u06cc\u0642\u0647 \u0648 \u062c\u0631\u06cc\u0645\u0647 {new_fine} \u0634\u062f.")

    elif query.data == "pay_fine":
        if user["points"] >= user["prison_fine"]:
            update_user(user_id, points=user["points"] - user["prison_fine"], prison_until=0, prison_fine=0)
            await query.edit_message_text("\u062c\u0631\u06cc\u0645\u0647 \u067e\u0631\u062f\u0627\u062e\u062a \u0634\u062f \u0648 \u0622\u0632\u0627\u062f \u0634\u062f\u06cc\u062f.")
        else:
            await query.edit_message_text("\u0645\u0648\u062c\u0648\u062f\u06cc \u06a9\u0627\u0611\u06cc \u0646\u06cc\u0633\u062a.")