import glob
import hashlib
import os
import sys


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def files_equals(fname1, fname2, chunk_size=4096) -> bool:
    with open(fname1, "rb") as f1, open(fname2, "rb") as f2:
        while (chunk1 := f1.read(chunk_size)) and (chunk2 := f2.read(chunk_size)):
            if chunk1 != chunk2:
                return False
    return True


def get_files(dir):
    files = []
    for filename in glob.iglob(dir + '**/**', recursive=True):
        if os.path.isfile(filename):
            files.append(filename)

    return files


args = sys.argv

if len(args) != 3:
    raise ValueError("Wrong number of args")

dir1 = args[1]
dir2 = args[2]

log_dir = "mismatch.txt"

print(f"Getting files from {dir1}")
files = get_files(dir1)
i = 0

print("Comparing hashes")
mismatch = 0

if os.path.exists("mismatch.txt"):
    os.remove("mismatch.txt")

for f in files:
    if i % 100 == 0:
        print(f"{i}/{len(files)}")

    other_file = dir2 + f[len(dir1):]

    if not files_equals(f, other_file):
        mismatch += 1
        with open(log_dir, "a") as log_f:
            msg = f"{dir2[0]}{f[1:]}\n"
            print(msg)
            log_f.write(msg)

    i += 1

if mismatch == 0:
    print("No mismatch found")
else:
    print(f"{mismatch} mismatches found")
