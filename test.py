import argparse
import time
import progressbar
from progressbar import ProgressBar


parser = argparse.ArgumentParser(description="Generate hashes for all files in a directory recursively.")
parser.add_argument("-d", type=str, help="The directory to be scanned.")
parser.add_argument("-h", type=str, help="The file containing the hash values.")

args = parser.parse_args()
print(args.d)
