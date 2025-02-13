import logging
import os
from datetime import datetime
from util import get_files

logging.basicConfig(encoding='utf-8',
                    level=logging.INFO,
                    # filemode="w",
                    handlers=[
                        logging.FileHandler("logs/get_most_recent_file.log"),
                        logging.StreamHandler()
                    ])

dir = "x:/"

files, _ = get_files(dir)
dates = []

for file in files:
    dates.append(int(os.path.getmtime(file)))

time = max(dates)
dt_object = datetime.fromtimestamp(time)
logging.info(f"Most recent date for {dir}")
logging.info(time)
logging.info(dt_object)
