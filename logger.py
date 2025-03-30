import logging
from datetime import datetime


logging.basicConfig(filename=f"./logs/{datetime.now().strftime('%Y-%m-%d')}.log",
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    filemode="a")

Logger = logging.getLogger()
Logger.setLevel(logging.DEBUG)
