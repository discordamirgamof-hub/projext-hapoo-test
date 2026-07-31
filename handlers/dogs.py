from aiogram import Router, F
from aiogram.types import Message
from db import get_user_data

router = Router()

DOGS_TEMPLATE = (
    "\U0001F415 \u0633\u06af\u200c\u0647\u0627\u06cc \u0634\u0645\u0627 \U0001F43E\n"
    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
    "\U0001F436 \u0633\u06af \u0641\u0639\u0627\u0644 : {dog_name}\n"
    "\u26A1 \u0642\u062f\u0631\u062a : {power}\n"
    "\U0001F3C6 \u062a\u0639\u062f\u0627\u062f \u0633\u06af\u200c\u0647\u0627 : {count}"
)

@router.message(F.text.lower().in_(["\u0633\u06af\u0647\u0627", "\u0633\u06af", "/dogs"]))
async def dogs_handler(message: Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    
    dog_name = user_data.get("active_dog", "\u0647\u0627\u067e\u0648\u06cc\u06cc \u06a9\u0648\u0686\u06a9")
    power = user_data.get("dog_power", 10)
    count = user_data.get("dog_count", 1)
    
    await message.reply(
        DOGS_TEMPLATE.format(
            dog_name=dog_name,
            power=power,
            count=count
        )
    )
