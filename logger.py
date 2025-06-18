import os
import logging
from datetime import datetime

if not os.path.exists("./logs/"):
    os.makedirs("./logs/")

logging.basicConfig(filename=f"./logs/{datetime.now().strftime('%Y-%m-%d')}.log",
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    filemode="a")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
