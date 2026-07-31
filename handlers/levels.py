from aiogram import Router, F
from aiogram.types import Message
from db import get_user_data

router = Router()

PROFILE_TEMPLATE = (
    "\U0001F48D \u067e\u0631\u0648\u0641\u0627\u06cc\u0644 \u06a9\u0627\u0631\u0628\u0631\u06cc \U0001F43E\n"
    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
    "\U0001F464 \u06a9\u0627\u0631\u0628\u0631 : {name}\n"
    "\u2B50 \u0633\u0637\u062d (\u0644\u0648\u0644) : {level}\n"
    "\u2728 \u0627\u0645\u062a\u06cc\u0627\u0632 (XP) : {xp}\n"
    "\U0001FA99 \u0647\u0627\u067e \u067e\u0648\u06cc\u0646\u062a : {hap_points:,}"
)

@router.message(F.text.lower().in_(["\u0644\u0648\u0644", "\u067e\u0631\u0648\u0641\u0627\u06cc\u0644", "/profile", "/level"]))
async def profile_handler(message: Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    
    name = message.from_user.first_name
    level = user_data.get("level", 1)
    xp = user_data.get("xp", 0)
    hap_points = user_data.get("hap_points", 0)
    
    await message.reply(
        PROFILE_TEMPLATE.format(
            name=name,
            level=level,
            xp=xp,
            hap_points=hap_points
        )
    )import time

def check_level_access(user, required_level):
    return user["level"] >= required_level

def is_in_prison(user):
    return time.time() < user["prison_until"]
