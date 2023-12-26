import logging
from datetime import datetime
from time import mktime

import progressbar
from exif import Image
from progressbar import ProgressBar

from util import get_files
import os
import shutil


def is_video(file):
    types = {'webm', 'mkv', 'flv', 'vob', 'ogv', 'ogg', 'rrc', 'gifv', 'mng', 'mov', 'avi', 'qt', 'wmv', 'yuv', 'rm',
             'asf', 'amv', 'mp4', 'm4p', 'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'm4v', 'svi', '3gp', '3g2', 'mxf',
             'roq', 'nsv', 'flv', 'f4v', 'f4p', 'f4a', 'f4b', 'mod'}

    _, ext = os.path.splitext(file)
    return ext[1:] in types


def is_image(file):
    types = {'.heic', '.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm',
             '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm'}
    _, ext = os.path.splitext(file)
    return ext in types


def get_time(file: str) -> int:
    with open(file, 'rb') as image_file:
        try:
            img = Image(image_file)
        except:
            return int(os.path.getmtime(file))

    if not is_image(file) or not is_video(file) or not img.has_exif or 'datetime' not in img.list_all():
        return int(os.path.getmtime(file))

    return int(mktime(datetime.strptime(img.datetime, "%Y:%m:%d %H:%M:%S").timetuple()))


progressbar.streams.wrap_stderr()
logging.basicConfig(encoding='utf-8',
                    level=logging.INFO,
                    # filemode="w",
                    handlers=[
                        logging.FileHandler("logs/copy_files_older_than.log"),
                        logging.StreamHandler()
                    ])

time = 1671205474
src = "Y:/Photos/DCIM"
dest = "D:/nas_bilder"

logging.info("Scanning files")
files, _ = get_files(src)
dates: list[tuple[int, str]] = []

logging.info("Retrieving timestamp from files")

for f in files:
    dates.append((get_time(f), f))

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
