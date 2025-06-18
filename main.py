import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from os import getenv

from handler import dp, setBotClass
from logger import logger
import DataManager
import scheduler

TOKEN = getenv("TIH365TOKEN")


async def main():
    logger.info("\n\n\n\n\nScript started")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    setBotClass(bot)
    asyncio.create_task(DataManager.autoSaveTask())
    asyncio.create_task(scheduler.timerTask())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
