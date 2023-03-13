import hashlib
import sys

from util import get_files, md5, progressBar

args = sys.argv

if len(args) != 2:
    raise ValueError("Wrong number of args")

root_dir = args[1]

files, _ = get_files(root_dir)
hash_file = "file_hashes.txt"

for f in progressBar(files,
                     prefix="Progress:",
                     # suffix=f"Complete {convert_size(bytes_scanned)}/{convert_size(total_size)}",
                     length=50,
                     # printEnd="",
                     buffer=None):
    hash_md5 = md5(f)
    rel_path = f[len(root_dir):]
    path_hash = hashlib.md5(rel_path.encode("UTF-8"))

    with open(hash_file, "a") as hf:
        hf.write(f"{path_hash.hexdigest()} {hash_md5}\n")
