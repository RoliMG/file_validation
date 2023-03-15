import hashlib
import logging
import os
import sys

import progressbar
from progressbar import ProgressBar

from util import get_files, convert_size


def file_equals(fname1: str, fname2: str, chunk_size: int = 4096) -> (bool, str):
    hash_md5 = hashlib.md5()

    try:
        with open(fname1, "rb") as f1, open(fname2, "rb") as f2:
            while (chunk1 := f1.read(chunk_size)) and (chunk2 := f2.read(chunk_size)):
                hash_md5.update(chunk1)

                if chunk1 != chunk2:
                    return False, ""
    except IOError:
        return False, ""

    return True, hash_md5.hexdigest()


args = sys.argv

if len(args) != 3:
    raise ValueError("Wrong number of args")

progressbar.streams.wrap_stderr()
logging.basicConfig(encoding='utf-8',
                    level=logging.INFO,
                    # filemode="w",
                    handlers=[
                        logging.FileHandler("logs/validate_directories.log"),
                        logging.StreamHandler()
                    ])

dir1 = args[1]
dir2 = args[2]

hash_file = "file_hashes.txt"

if os.path.exists(hash_file):
    os.remove(hash_file)

logging.info("Getting file list")
files, total_size = get_files(dir1)

widgets = [
    progressbar.Percentage(),
    progressbar.Bar(),
    ' [', progressbar.DataSize(prefixes=('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')), f'/{convert_size(total_size)}] ',
    ' (', progressbar.ETA(), ') ',
]

pbar = ProgressBar(max_value=total_size, widgets=widgets)
bytes_scanned = 0

logging.info(f"Comparing {len(files)} files ({convert_size(total_size)})")
corrupted_count = 0

for f in files:
    other_file = dir2 + f[len(dir1):]
    equals, hash_md5 = file_equals(f, other_file)

    if equals:
        with open(hash_file, "a") as hash_file_handler:
            hash_file_handler.write(f"{f[len(dir1):]}:{hash_md5}\n")
    else:
        corrupted_count += 1
        logging.warning(f"Mismatch found for {f}")

    bytes_scanned += os.path.getsize(f)
    pbar.update(bytes_scanned)

logging.info(f"Corruptions found {corrupted_count}")
