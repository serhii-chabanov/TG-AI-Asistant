import html
import asyncio
from aiogram import Dispatcher, types
import re

from config import config
from ai.manager import ai
from hardware_monitor import check_hardware
from scheduler import setup_scheduler

dp = Dispatcher()


@dp.message()
async def handle_message(message: types.Message):
    if message.from_user.id not in config.allowed_users:
        await message.answer("You dont have access to bot, sorry bro.")
        return

    try:
        response = await ai.get_response(message.text, message.from_user.id)

        if response:
            await message.answer(response)
        else:
            await message.answer("❌ Error in answering")

    except Exception as e:
        error_message = html.escape(str(e))
        await message.answer(f"❌ **Error:**\n<code>{error_message}</code>")
        print(f"Error logs: {e}")


async def main():
    admin_id = config.allowed_users[0] if config.allowed_users else 0
    
    if admin_id:
        asyncio.create_task(check_hardware(config.bot, admin_id))
        setup_scheduler(config.bot, admin_id)
    
    print("🚀 Bot starting...")
    await dp.start_polling(config.bot)


if __name__ == "__main__":
    asyncio.run(main())