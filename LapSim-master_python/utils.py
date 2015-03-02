from functools import wraps
import os


class RangeFloat:
    def __init__(self, low, high, step=1):
        self.current = low
        self.high = high
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += self.step
            return self.current - self.step


def memoize(f):
    d = {}

    @wraps(f)
    def wrapper(*args):
        if args not in d:
            d[args] = f(*args)
        return d[args]

    return wrapper


def ensure_dir(f):
    d = os.path.dirname(f)
    while not os.path.exists(d):
        os.makedirs(d)