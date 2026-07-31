import re
from telegram import Update
from telegram.ext import ContextTypes
from db import get_user, update_user, add_xp, set_pending_bet, get_pending_bet, clear_pending_bet
from handlers.levels import check_level_access, is_in_prison
from config import LEVEL_CASINO, CASINO_XP_REWARD

def parse_bet_amount(text: str) -> int:
    text = text.replace(";", "").replace(",", "").strip().lower()
    match = re.match(r"^(\d+(?:\.\d+)?)\s*([km])?$", text)
    if not match:
        return None
    val, suffix = match.groups()
    val = float(val)
    if suffix == "k":
        val *= 1_000
    elif suffix == "m":
        val *= 1_000_000
    return int(val)

async def casino_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    if not check_level_access(user, LEVEL_CASINO):
        await update.message.reply_text("\u06a9\u0627\u0632\u06cc\u0646\u0648 \u0627\u0632 \u0633\u0637\u062d \u06f3 \u0628\u0627\u0632 \u0645\u06cc\u200c\u0634\u0648\u062f.")
        return

    text = (
        "\u0628\u0647 \u06a9\u0627\u0632\u06cc\u0646\u0648 \u062e\u0648\u0634 \u0622\u0645\u062f\u06cc\u062f!\n"
        "\u0628\u0631\u0627\u06cc \u0628\u0627\u0632\u06cc \u062a\u0627\u0633\u060c \u0645\u0628\u0644\u063a \u0634\u0631\u0637 \u0631\u0627 \u0631\u06cc\u06e2\u067e\u0644\u0627\u06cc \u06a9\u0646\u06cc\u062f (\u0645\u062b\u0644\u0627 50k \u06cc\u0627 50;000) \u0648 \u06a9\u0644\u0645\u0647 \u0632\u0648\u062c \u0b10 \u0641\u0631\u062f \u0631\u0627 \u0628\u0646\u0648\u06cc\u0633\u06cc\u062f\u060c \u0633\u067e\u0633 \u0627\u06cc\u0645\u0648\u062c\u06cc \ud83c\udfb2 \u0628\u0641\u0631\u0633\u062a\u06cc\u062f.\n"
        "\u0628\u0631\u0627\u06cc \u0627\u0633\u0644\u0627\u062a\u060c \u0645\u0628\u0644\u063a \u0631\u0627 \u0631\u06cc\u06e2\u067e\u0644\u0627\u06cc \u06a9\u0631\u062f\u0647 \u0648 \u0627\u06cc\u0645\u0648\u062c\u06cc \ud83c\udfb0 \u0628\u0641\u0631\u0633\u062a\u06cc\u062f."
    )
    await update.message.reply_text(text)

async def reply_bet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not check_level_access(user, LEVEL_CASINO) or is_in_prison(user):
        return

    text = update.message.text.strip()
    prediction = None

    if "\u0632\u0648\u062c" in text:
        prediction = "even"
        text = text.replace("\u0632\u0648\u062c", "")
    elif "\u0641\u0631\u062f" in text:
        prediction = "odd"
        text = text.replace("\u0641\u0631\u062f", "")

    amount = parse_bet_amount(text)
    if amount is None or amount <= 0:
        return

    if amount > user["points"]:
        await update.message.reply_text("\u0645\u0648\u062c\u0648\u062f\u06cc \u06a9\u0627\u0611\u06cc \u0646\u06cc\u0633\u062a.")
        return

    set_pending_bet(user_id, "pending", amount, prediction)
    await update.message.reply_text(f"\u0634\u0631\u0637 {amount} \u062b\u0628\u062a \u0634\u062f. \u062d\u0627\u0644\u0627 \u0627\u06cc\u0645\u0648\u062c\u06cc \ud83c\udfb2 \u06cc\u0627 \ud83c\udfb0 \u0631\u0627 \u0628\u0641\u0631\u0633\u062a\u06cc\u062f.")

async def dice_emoji_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    bet = get_pending_bet(user_id)
    if not bet:
        return

    bet_amount = bet["bet_amount"]
    prediction = bet["prediction"]
    value = update.message.dice.value
    add_xp(user_id, CASINO_XP_REWARD)

    is_even = (value % 2 == 0)
    win = False
    if prediction == "even" and is_even:
        win = True
    elif prediction == "odd" and not is_even:
        win = True

    if win:
        new_points = user["points"] + bet_amount
        update_user(user_id, points=new_points)
        await update.message.reply_text(f"\u062a\u0627\u0633 {value} \u0622\u0645\u062f! \u0634\u0645\u0627 \u0628\u0631\u0646\u062f\u0647 {bet_amount} \u067e\u0648\u06cc\u0646\u062a \u0634\u062f\u06cc\u062f.")
    else:
        new_points = user["points"] - bet_amount
        update_user(user_id, points=new_points)
        await update.message.reply_text(f"\u062a\u0627\u0633 {value} \u0622\u0645\u062f! \u0634\u0645\u0627 \u0628\u0627\u062e\u062a\u06cc\u062f.")

    clear_pending_bet(user_id)

async def slot_emoji_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    bet = get_pending_bet(user_id)
    if not bet:
        return

    bet_amount = bet["bet_amount"]
    value = update.message.dice.value
    add_xp(user_id, CASINO_XP_REWARD)

    if value == 64:  # Jackpot 777
        win_amount = bet_amount * 5
        update_user(user_id, points=user["points"] + win_amount)
        await update.message.reply_text(f"\u062c\u06a9\u200c\u067e\u0627\u062a! \u0634\u0645\u0627 {win_amount} \u0628\u0631\u0646\u062f\u0647 \u0634\u062f\u06cc\u062f.")
    elif value == 1:  # BAR symbol
        win_amount = bet_amount * 2
        update_user(user_id, points=user["points"] + win_amount)
        await update.message.reply_text(f"\u0646\u0645\u0627\u062f BAR! \u0634\u0645\u0627 {win_amount} \u0628\u0631\u0646\u062f\u0647 \u0634\u062f\u06cc\u062f.")
    else:
        update_user(user_id, points=user["points"] - bet_amount)
        await update.message.reply_text("\u0634\u0645\u0627 \u0628\u0627\u062e\u062a\u06cc\u062f.")

    clear_pending_bet(user_id)