import time
import random
from aiogram import Router, F
from aiogram.types import Message
from db import update_user_hap, get_user_data

router = Router()

# Cooldown duration in seconds (5 minutes = 300 seconds)
HAP_COOLDOWN_SECONDS = 300

# Dictionary to store last claim timestamps
user_cooldowns = {}

# Message templates (Unicode encoded for clean execution)
SUCCESS_MSG_TEMPLATE = (
    "{points} \u0647\u0627\u067e \u067e\u0648\u06cc\u0646\u062a \u06AF\u0631\u0641\u062A\u06CC \U0001F43E\n"
    "\U0001F4B0 \u0647\u0627\u067e \u067e\u0648\u06cc\u0646\u062a \u0647\u0627\u062A : {total:,} \U0001FA99\n"
    "\u23f3 \u0628\u0639\u062f \u0627\u0632 {time_str} \u0645\u06cc\u062a\u0648\u0646\u06cc \u062f\u0648\u0628\u0627\u0631\u0647 \u0647\u0627\u067e \u0647\u0627\u067e \u06A9\u0646\u06cc"
)

COOLDOWN_MSG_TEMPLATE = (
    "\u23f3 \u0628\u0639\u062f \u0627\u0632 {time_str} \u0645\u06cc\u062a\u0648\u0646\u06cc \u062f\u0648\u0628\u0627\u0631\u0647 \u0647\u0627\u067e \u0647\u0627\u067e \u06A9\u0646\u06cc"
)

def format_time(seconds: int) -> str:
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"

@router.message(F.text.lower().in_(["\u0647\u0627\u067e", "hap", "/hap"]))
async def hap_command_handler(message: Message):
    user_id = message.from_user.id
    current_time = time.time()

    # Check cooldown status
    if user_id in user_cooldowns:
        elapsed = current_time - user_cooldowns[user_id]
        if elapsed < HAP_COOLDOWN_SECONDS:
            remaining = int(HAP_COOLDOWN_SECONDS - elapsed)
            time_str = format_time(remaining)
            await message.reply(COOLDOWN_MSG_TEMPLATE.format(time_str=time_str))
            return

    # Random reward points between 10 and 90
    gained_points = random.randint(10, 90)
    
    # Save to database and retrieve updated total
    user_total_points = update_user_hap(user_id, gained_points)
    
    # Update cooldown timestamp
    user_cooldowns[user_id] = current_time
    
    time_str = format_time(HAP_COOLDOWN_SECONDS)
    
    response_text = SUCCESS_MSG_TEMPLATE.format(
        points=gained_points,
        total=user_total_points,
        time_str=time_str
    )
    
    await message.reply(response_text)
