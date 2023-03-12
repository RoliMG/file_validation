import hashlib
import sys
from pathlib import Path

args = sys.argv

if len(args) != 3:
    raise ValueError("Wrong number of args")

root_dir = args[1]
hash_file = args[2]

file_hashes: dict[Path, str] = dict()

with open(hash_file, "r") as f:
    line = f.readline()
    separator_index = line.index(":")
    file_full_path = Path(f"{root_dir}/{line[:separator_index]}")
    file_hashes[file_full_path] = line[separator_index+1:len(line)-1]

for (path, file_hash) in file_hashes.items():
    hash_md5 = hashlib.md5()

    with open(path, "rb") as f:
        hash_md5.update(f.read(4096))

    if file_hash != hash_md5.hexdigest():
        print(f"Files not equal {path}")
