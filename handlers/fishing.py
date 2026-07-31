import random
from aiogram import Router, F
from aiogram.types import Message
from db import update_user_hap

router = Router()

FISHING_SUCCESS = (
    "\U0001F3A3 \u06cc\u06a9 \u0645\u0627\u0647\u06cc \u0635\u06cc\u062f \u06a9\u0631\u062f\u06cc! \U0001F41F\n"
    "\U0001F4B0 \u0627\u0631\u0632\u0634 \u0635\u06cc\u062f : {reward} \u0647\u0627\u067e \u067e\u0648\u06cc\u0646\u062a \U0001FA99\n"
    "\U0001F4B8 \u0645\u0648\u062c\u0648\u062f\u06cc \u06a9\u0644 : {total:,} \U0001FA99"
)

@router.message(F.text.lower().in_(["\u0645\u0627\u0647\u06cc\u06af\u06cc\u0631\u06cc", "fishing", "/fishing"]))
async def fishing_handler(message: Message):
    user_id = message.from_user.id
    reward = random.randint(15, 60)
    total = update_user_hap(user_id, reward)
    
    await message.reply(
        FISHING_SUCCESS.format(
            reward=reward,
            total=total
        )
    )
