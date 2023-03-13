import hashlib
import os
import sys

import math

from util import get_files, progressBar

suffix = "Complete"
bytes_scanned = 0


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


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

dir1 = args[1]
dir2 = args[2]

corrupted_log_file = "mismatch.txt"
hash_file = "file_hashes.txt"

print(f"Getting files from {dir1}")
files, total_size = get_files(dir1)
i = 0

print(f"Comparing {len(files)} files ({convert_size(total_size)})")
corrupted_count = 0

if os.path.exists(corrupted_log_file):
    os.remove(corrupted_log_file)

buffer = []

for f in progressBar(files,
                     prefix="Progress:",
                     # suffix=f"Complete {convert_size(bytes_scanned)}/{convert_size(total_size)}",
                     length=50,
                     # printEnd="",
                     buffer=buffer):
    other_file = dir2 + f[len(dir1):]
    equals, hash_md5 = file_equals(f, other_file)

    if equals:
        with open(hash_file, "a") as hash_file_handler:
            hash_file_handler.write(f"{f[len(dir1):]}:{hash_md5}\n")
    else:
        corrupted_count += 1
        with open(corrupted_log_file, "a") as log_f:
            buffer.append(f)
            log_f.write(f + "\n")

    bytes_scanned += os.path.getsize(f)
    suffix = f"Complete {convert_size(bytes_scanned)}/{convert_size(total_size)}"

if corrupted_count:
    print("No corruption found")
else:
    print(f"{corrupted_count} corruptions found")
