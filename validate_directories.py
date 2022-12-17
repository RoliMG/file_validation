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

    f_md5 = md5(f)
    other_file = dir2 + f[len(dir1):]
    f2_md5 = md5(other_file)

    if f_md5 != f2_md5:
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
