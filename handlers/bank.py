from aiogram import Router, F
from aiogram.types import Message
from db import get_user_data

router = Router()

BANK_TEMPLATE = (
    "\U0001F3E6 \u0628\u0627\u0646\u06a9 \u0647\u0627\u067e\u0648\u06cc\u06cc \U0001F43E\n"
    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
    "\U0001F4B0 \u0645\u0648\u062c\u0648\u062f\u06cc \u06a9\u06cc\u0641 \u067e\u0648\u0644 : {wallet:,} \U0001FA99\n"
    "\U0001F3E6 \u0645\u0648\u062c\u0648\u062f\u06cc \u0628\u0627\u0646\u06a9 : {bank:,} \U0001FA99\n"
    "\U0001F4A1 \u0645\u062c\u0645\u0648\u0639 \u062f\u0627\u0631\u0627\u06cc\u06cc : {total:,} \U0001FA99"
)

@router.message(F.text.lower().in_(["\u0628\u0627\u0646\u06a9", "/bank"]))
async def bank_handler(message: Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    
    wallet = user_data.get("hap_points", 0)
    bank_balance = user_data.get("bank_balance", 0)
    total = wallet + bank_balance
    
    await message.reply(
        BANK_TEMPLATE.format(
            wallet=wallet,
            bank=bank_balance,
            total=total
        )
    )
