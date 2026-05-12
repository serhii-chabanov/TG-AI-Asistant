import html
import asyncio
from aiogram import Dispatcher, types

from config import config
from ai.manager import ai

dp = Dispatcher()


@dp.message()
async def handle_message(message: types.Message):
    if message.from_user.id not in config.allowed_users:
        await message.answer("You dont have access to bot, sorry bro.")
        return

    try:
        response_text = await ai.get_response(message.text, message.from_user.id)

        if response_text:
            await message.answer(response_text)
        else:
            await message.answer("❌ Error in answering")

    except Exception as e:
        error_message = html.escape(str(e))
        await message.answer(f"❌ **Error:**\n<code>{error_message}</code>")
        print(f"Error logs: {e}")


async def main():
    await dp.start_polling(config.bot)


if __name__ == "__main__":
    asyncio.run(main())