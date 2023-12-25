import argparse
import time

import progressbar
from progressbar import ProgressBar

pbar = ProgressBar(max_value=100)

for i in range(100):
    pbar.update(i)
    time.sleep(1)
