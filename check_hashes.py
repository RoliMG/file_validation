import hashlib
import sys

from util import get_files, md5

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

files, _ = get_files(root_dir)

for f in files:
    rel_path = f[len(root_dir):]
    path_hash = hashlib.md5(rel_path.encode("UTF-8")).hexdigest()
    data_hash = md5(f)

    if path_hash not in file_hashes.keys():
        print(f"{f} not found in hash file")

    if file_hashes[path_hash] != data_hash:
        print(f"Hash mismatch {f}")

