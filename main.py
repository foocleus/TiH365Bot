import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from os import getenv

from handler import dp
from logger import Logger
import DataManager

TOKEN = getenv("TIH365TOKEN")


async def main():
    Logger.info("\n\n\n\n\nScript started")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.create_task(DataManager.autoSaveTask())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
