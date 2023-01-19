import math
import os

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def file_equals(fname1, fname2, chunk_size=4096) -> bool:
    sum_size = 0

    with open(fname1, "rb") as f1, open(fname2, "rb") as f2:
        while (chunk1 := f1.read(chunk_size)) and (chunk2 := f2.read(chunk_size)):
            if chunk1 != chunk2:
                return False

        sum_size += 4096

    print(f"\r{convert_size(sum_size)}")
    return True


f1 = "C:/Users/Roli/Desktop/Gabriela photos old CDs"
f2 = "D:/Gabriela photos old CDs"
print(f"Size: {convert_size(os.path.getsize(f1))}")

res = file_equals(f1, f2)

print(res)

