from smart_open import open
from contextlib import contextmanager


@contextmanager
def read_line(file_path):
    f = open(file_path)
    try:
        def gen():
            b = f.readline()
            while b:
                yield b
                b = f.readline()
        yield gen()
    finally:
        f.close()
