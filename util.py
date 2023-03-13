import hashlib
import math
import os


def get_files(dir: str):
    files = []
    total_size = 0

    for root, subdir, filenames in os.walk(dir):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            total_size += os.path.getsize(full_path)
            files.append(full_path)

    return files, total_size


def md5(fname: str):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"
