import logging
import os
import sys

import progressbar
from progressbar import ProgressBar

from util import get_files, md5, convert_size

args = sys.argv

if len(args) != 2:
    raise ValueError("Wrong number of args")

progressbar.streams.wrap_stderr()
logging.basicConfig(encoding='utf-8',
                    level=logging.INFO,
                    # filemode="w",
                    handlers=[
                        logging.FileHandler("logs/generate_hashes.log"),
                        logging.StreamHandler()
                    ])

SEPARATOR = ":"
root_dir = args[1]

logging.info("Getting file list")
files, total_size = get_files(root_dir)
hash_file = "file_hashes.txt"

if os.path.exists(hash_file):
    os.remove(hash_file)

widgets = [
    progressbar.Percentage(),
    progressbar.Bar(),
    ' [', progressbar.DataSize(prefixes=('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')), f'/{convert_size(total_size)}] ',
    ' (', progressbar.ETA(), ') ',
]

pbar = ProgressBar(max_value=total_size, widgets=widgets)
bytes_scanned = 0
open_errors = 0

logging.info(f"Generating hashes for {len(files)} files")
for f in files:
    hash_md5 = ""

    try:
        hash_md5 = md5(f)
    except IOError:
        logging.warning(f"Cannot open file {f}")
        open_errors += 1
        hash_md5 = "0"

    rel_path = f[len(root_dir):]

    bytes_scanned += os.path.getsize(f)
    pbar.update(bytes_scanned)

    try:
        with open(hash_file, "a", encoding="UTF-8") as hf:
            hf.write(f"{rel_path}{SEPARATOR}{hash_md5}\n")
    except IOError:
        logging.error(f"Could not access hash file: {hash_file}")

logging.info(f"Hash generation completed. File open errors: {open_errors}")
