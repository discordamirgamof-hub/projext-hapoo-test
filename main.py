from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from config import BOT_TOKEN
from db import init_db
from handlers import (
    start_handler,
    academy_handler,
    profile_handler,
    hap_handler,
    bank_handler,
    casino_handler,
    reply_bet_handler,
    dice_emoji_handler,
    slot_emoji_handler,
    fishing_handler,
    sell_fish_handler,
    inventory_fish_handler,
    smuggle_handler,
    prison_callback_handler,
)

def main():
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(MessageHandler(filters.Regex("^\u0647\u0627\u067e\u0648\u06cc\u06cc$|^\u0634\u0631\u0648\u0639 \u0647\u0627\u067e\u0648\u06cc\u06cc$"), start_handler))
    app.add_handler(MessageHandler(filters.Regex("^\u0622\u06a9\u0627\u062f\u0645\u06cc \u0647\u0627\u067e\u0648\u06cc\u06cc$"), academy_handler))
    app.add_handler(MessageHandler(filters.Regex("^\u067e\u0631\u0648\u0641\u0627\u06cc\u0644 \u0647\u0627\u067e\u0648\u06cc\u06cc$"), profile_handler))
    app.add_handler(MessageHandler(filters.Regex("^\u0647\u0627\u067e$"), hap_handler))
    app.add_handler(MessageHandler(filters.Regex("^\u0628\u0627\u0646\u06a9 \u0647\u0627\u067e\u0648\u06cc\u06cc$"), bank_handler))
    app.add_handler(MessageHandler(filters.Regex("^\u06a9\u0627\u0632\u06cc\u0646\u0648 \u0647\u0627\u067e\u0648\u06cc\u06cc$"), casino_handler))
    app.add_handler(MessageHandler(filters.Regex("^\u0645\u0627\u0647\u06cc\u06af\u06cc\u0631\u06cc \u0647\u0627\u067e\u0648\u06cc\u06cc$|^\u0645\u0627\u0647\u06cc\u06af\u06cc\u0631\u06cc$"), fishing_handler))
    app.add_handler(MessageHandler(filters.Regex("^\u0641\u0631\u0648\u0634 \u0645\u0627\u0647\u06cc$"), sell_fish_handler))
    app.add_handler(MessageHandler(filters.Regex("^\u0627\u0646\u0628\u0627\u0631 \u0645\u0627\u0647\u06cc$"), inventory_fish_handler))
    app.add_handler(MessageHandler(filters.Regex("^\u0642\u0627\u062d\u0627\u0642 \u0647\u0627\u067e\u0648\u06cc\u06cc$"), smuggle_handler))

    app.add_handler(MessageHandler(filters.Dice.DICE, dice_emoji_handler))
    app.add_handler(MessageHandler(filters.Dice.SLOT_MACHINE, slot_emoji_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_bet_handler))
    app.add_handler(CallbackQueryHandler(prison_callback_handler))

    app.run_polling()

if __name__ == "__main__":
    main()