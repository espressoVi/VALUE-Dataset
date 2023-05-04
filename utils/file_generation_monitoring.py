import os
from time import perf_counter, sleep
import re, sys
from colorist import Color

class Reprinter:
    def __init__(self):
        self.text = ''
    def write(self, text):
        sys.stdout.write(text)
        sys.stdout.flush()
    def cursor_prev_line(self):
        self.write("\x1b[A")
    def cursor_prev_line_start(self):
        self.write("\x1b[F")
    def cursor_line_start(self):
        self.write("\r")
    def cursor_text_start(self):
        num_newlines = self.text.count("\n")
        if not num_newlines:
            return self.cursor_line_start()
        for _ in range(num_newlines):
            self.cursor_prev_line_start()
    def erase(self):
        self.cursor_text_start()
        self.write(re.sub(r"[^\s]", " ", self.text))
        self.cursor_text_start()
    def __call__(self, text):
        self.erase()
        self.write(text)
        self.text = text

class MultiStatus:
    def __init__(self):
        self.print = Reprinter()
        self.file = './run.sh'
        self.dir = './images/'
        self.samples_per_min = 6
    def _read_range(self):
        with open(self.file, 'r') as f:
            lines = f.readlines()[1:]
        lines = [i.strip().split()[6:8] for i in lines] 
        lines = [(int(i[0]), int(i[1])) for i in lines]
        return lines
    def range_counter(self):
        self.ranges = self._read_range()
        range_counter = {i:0 for i in self.ranges}
        files = [int(i[3:-4]) for i in os.listdir(self.dir)]
        for file in files:
            for low, high in self.ranges:
                range_counter[(low, high)] += 1 if low <= file < high else 0
        return range_counter
    def measure_rate(self):
        start = self.range_counter()
        sleep(60//self.samples_per_min)
        end = self.range_counter()
        rate = {key:self.samples_per_min*(end[key]-val) for key,val in start.items()}
        return rate,end
    def __call__(self):
        res = []
        rate,counts = self.measure_rate()
        for low,high in self.ranges: 
            res.append(f'{Color.CYAN}In {low} -> {high}\t:{Color.OFF} {counts[(low,high)]:07d} ({100*counts[(low,high)]/(high-low):.1f}%) done at \t\t {Color.RED}{rate[(low,high)]} images per minute{Color.OFF}')
        status = '\n'.join(res)
        self.print(status)

if __name__ == "__main__":
    status = MultiStatus()
    while True:
        status()
