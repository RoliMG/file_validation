import hashlib
import logging
import os
import sys

import progressbar
from progressbar import ProgressBar

from util import get_files, md5, convert_size

args = sys.argv

if len(args) != 3:
    raise ValueError("Wrong number of args")

progressbar.streams.wrap_stderr()
logging.basicConfig(encoding='utf-8',
                    level=logging.INFO,
                    # filemode="w",
                    handlers=[
                        logging.FileHandler("logs/check_hashes.log"),
                        logging.StreamHandler()
                    ])

SEPARATOR = ":"

root_dir = args[1]
hash_file = args[2]

file_hashes: dict[str, str] = dict()

try:
    with open(hash_file, "r", encoding="UTF-8") as f:
        while line := f.readline():
            separator_index = line.index(SEPARATOR)
            file_path = line[:separator_index]
            file_hashes[file_path] = line[separator_index + 1:len(line) - 1]
except IOError:
    logging.error(f"Could not open {hash_file}")

logging.info("Getting file list")
files, total_size = get_files(root_dir)

widgets = [
    progressbar.Percentage(),
    progressbar.Bar(),
    ' [', progressbar.DataSize(prefixes=('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')), f'/{convert_size(total_size)}] ',
    ' (', progressbar.ETA(), ') ',
]

pbar = ProgressBar(max_value=total_size, widgets=widgets)
bytes_scanned = 0
mismatch = 0

logging.info(f"Checking Hashes for {len(files)} files")
for f in files:
    rel_path = f[len(root_dir):]
    data_hash = md5(f)

    if rel_path not in file_hashes.keys():
        logging.warning(f"{f} not found in hash file")

    if rel_path in file_hashes.keys() and file_hashes[rel_path] != data_hash:
        logging.warning(f"Hash mismatch {f}")
        mismatch += 1

    bytes_scanned += os.path.getsize(f)
    pbar.update(bytes_scanned)

logging.info(f"Checking hashes completed. Found mismatches: {mismatch}")
