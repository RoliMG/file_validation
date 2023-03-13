import hashlib
import os

from validate_directories import suffix


def get_files(dir: str):
    files = []
    total_size = 0

    for root, subdir, filenames in os.walk(dir):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            total_size += os.path.getsize(full_path)
            files.append(full_path)

    return files, total_size


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


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

        [print(f"\r{b}{' ' * 150}\n", end=printEnd) for b in buffer]
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
