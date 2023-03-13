import os
import sys

import progressbar
from progressbar import ProgressBar

from util import get_files, md5, convert_size

args = sys.argv

if len(args) != 2:
    raise ValueError("Wrong number of args")

SEPARATOR = ":"
root_dir = args[1]

files, total_size = get_files(root_dir)
hash_file = "file_hashes.txt"

if os.path.exists(hash_file):
    os.remove(hash_file)

widgets = [
    progressbar.Percentage(),
    progressbar.Bar(),
    ' [', progressbar.DataSize(), f'/{convert_size(total_size)}] ',
    ' (', progressbar.ETA(), ') ',
]

pbar = ProgressBar(max_value=total_size, widgets=widgets)
errors = []
sum_size = 0

for f in files:
    hash_md5 = ""

    try:
        hash_md5 = md5(f)
    except IOError:
        errors.append(f"Cannot open file {f}")

    rel_path = f[len(root_dir):]

    sum_size += os.path.getsize(f)
    pbar.update(sum_size)

    with open(hash_file, "a", encoding="UTF-8") as hf:
        hf.write(f"{rel_path}{SEPARATOR}{hash_md5}\n")
