import os
import time
from datetime import datetime


def get_date(file: str) -> int:
    with open(file, 'rb') as image_file:
        img = Image(image_file)

    if not img.has_exif or 'datetime' not in set(img.list_all()):
        return int(os.path.getmtime(file))

    return int(time.mktime(datetime.strptime(img.datetime, "%Y:%m:%d %H:%M:%S").timetuple()))


print(get_date("pic2.jpg"))
