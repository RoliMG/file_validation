import glob
import hashlib
import os
import sys

import math

suffix = "Complete"
bytes_scanned = 0


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def progressBar(iterable, prefix='', decimals=1, length=100, fill='█', printEnd="\r", buffer=None):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    if buffer is None:
        buffer = []

    total = len(iterable)

    # Progress Bar Printing Function
    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)

        [print(f"\r{b}{' ' * 100}\n", end=printEnd) for b in buffer]
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        buffer.clear()

    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def file_equals(fname1, fname2, chunk_size=4096) -> bool:
    with open(fname1, "rb") as f1, open(fname2, "rb") as f2:
        while (chunk1 := f1.read(chunk_size)) and (chunk2 := f2.read(chunk_size)):
            if chunk1 != chunk2:
                return False
    return True


def get_files(dir):
    files = []
    total_size = 0

    for filename in glob.iglob(dir + '**/**', recursive=True):
        if os.path.isfile(filename):
            total_size += os.path.getsize(filename)
            files.append(filename)

    return files, total_size


args = sys.argv

if len(args) != 3:
    raise ValueError("Wrong number of args")

dir1 = args[1]
dir2 = args[2]

mismatches_file = "mismatch.txt"
checked_file = "checked.txt"

print(f"Getting files from {dir1}")
files, total_size = get_files(dir1)
i = 0

print(f"Comparing {len(files)} files ({convert_size(total_size)})")
mismatches = []

if os.path.exists(mismatches_file):
    os.remove(mismatches_file)

buffer = []

for f in progressBar(files,
                     prefix="Progress:",
                     # suffix=f"Complete {convert_size(bytes_scanned)}/{convert_size(total_size)}",
                     length=50,
                     # printEnd="",
                     buffer=buffer):
    other_file = dir2 + f[len(dir1):]

    if not file_equals(f, other_file):
        mismatches.append(f)
        with open(mismatches_file, "a") as log_f:
            buffer.append(f)
            log_f.write(f + "\n")

    bytes_scanned += os.path.getsize(f)
    suffix = f"Complete {convert_size(bytes_scanned)}/{convert_size(total_size)}"

if not mismatches:
    print("No mismatch found")
else:
    print(f"{len(mismatches)} mismatches found")
