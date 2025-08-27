import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from os import getenv
from test import TEST_TOKEN

from handler import dp, setBotClass, tryAnnouncing
from logger import logger
import DataManager
import scheduler

#TOKEN = getenv("TIH365TOKEN")


async def main():
    logger.info("\n\n\n\n\nScript started")
    bot = Bot(token=TEST_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    setBotClass(bot)
    await tryAnnouncing()
    asyncio.create_task(DataManager.autoSaveTask())
    asyncio.create_task(scheduler.timerTask())
    print("Started polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
