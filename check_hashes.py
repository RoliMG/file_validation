import hashlib
import os
import sys

from progressbar import ProgressBar

from util import get_files, md5, convert_size

args = sys.argv

if len(args) != 3:
    raise ValueError("Wrong number of args")

root_dir = args[1]
hash_file = args[2]

file_hashes: dict[str, str] = dict()

with open(hash_file, "r") as f:
    while line := f.readline():
        separator_index = line.index(" ")
        file_path_hash = line[:separator_index]
        file_hashes[file_path_hash] = line[separator_index + 1:len(line) - 1]

files, total_size = get_files(root_dir)

pbar = ProgressBar(max_value=len(files))
bytes_scanned = 0

for f in files:
    rel_path = f[len(root_dir):]
    path_hash = hashlib.md5(rel_path.encode("UTF-8")).hexdigest()
    data_hash = md5(f)
    msg = []

    if path_hash not in file_hashes.keys():
        msg.append(f"{f} not found in hash file")

    if path_hash in file_hashes.keys() and file_hashes[path_hash] != data_hash:
        msg.append(f"Hash mismatch {f}")

    bytes_scanned += os.path.getsize(f)
    suffix = f"Complete {convert_size(bytes_scanned)}/{convert_size(total_size)}"
    pbar.tick(msg, suffix)

