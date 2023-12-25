import logging

import progressbar
from progressbar import ProgressBar

from util import get_files
import os
import shutil

progressbar.streams.wrap_stderr()
logging.basicConfig(encoding='utf-8',
                    level=logging.INFO,
                    # filemode="w",
                    handlers=[
                        logging.FileHandler("logs/copy_files_older_than.log"),
                        logging.StreamHandler()
                    ])

time = 1671205474
src = "Y:/Photos"
dest = "D:/nas_bilder"

logging.info("Scanning files")
files, _ = get_files(src)
dates: list[tuple[int, str]] = []

for file in files:
    dates.append((int(os.path.getmtime(file)), file))

most_recent = [f[1] for f in dates if f[0] > time]


pbar = ProgressBar(max_value=len(most_recent))

i = 0

logging.info("Copying files")

for src_file in most_recent:
    dest_path = os.path.dirname(src_file).replace(src, dest)
    os.makedirs(dest_path, exist_ok=True)

    shutil.copy2(src_file, dest_path)
    i += 1
    pbar.update(i)

pbar.finished()
