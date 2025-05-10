import asyncio
from datetime import datetime

from handler import sendScheduledMessages
import DataManager


async def timerTask():
    while True:
        now = datetime.now()
        await asyncio.sleep(3600 - now.minute * 60 - now.second + 5)
        ids = DataManager.getIdsByValue("scheduledHour", datetime.now().hour)
        await sendScheduledMessages(ids)