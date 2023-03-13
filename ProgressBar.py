from typing import Iterable


class ProgressBar:
    def __init__(self, iterable: Iterable, prefix: str = '', decimals: int = 1, length: int = 100, fill: str = '█',
                 print_end: str = "\r"):
        """
        @params:
            iterable    - Required  : iterable object (Iterable)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        self._iterable = iterable
        self._prefix = prefix
        self._decimals = decimals
        self._length = length
        self._fill = fill
        self._print_end = print_end
        self._data_counter = 0

    def _print_progress_bar(self, iteration: int, buffer: list, suffix: str):
        total = len(self._iterable)
        percent = ("{0:." + str(self._decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(self._length * iteration // total)
        bar = self._fill * filledLength + '-' * (self._length - filledLength)

        [print(f"\r{b}{' ' * 150}\n", end=self._print_end) for b in buffer]
        print(f'\r{self._prefix} |{bar}| {percent}% {suffix}', end=self._print_end)
        buffer.clear()

    def tick(self, buffer: list, suffix: str):
        if buffer is None:
            buffer = []

        self._print_progress_bar(self._data_counter, buffer, suffix)
        self._data_counter += 1

        # Print New Line on Complete
        print()
