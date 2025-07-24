import os
from typing import Generator

def deco(color: str):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "end": "\033[0m"
    }
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(colors.get(color, ""), end="")
            result = func(*args, **kwargs)
            print(colors["end"], end="")
            return result
        return wrapper
    return decorator

class Filer:
    def __init__(self, filename: str):
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    def line_generator(self) -> Generator[str, None, None]:
        with open(self.filename, 'r') as f:
            for line in f:
                yield line.strip()

    def __iter__(self):
        self._file = open(self.filename)
        return self

    def __next__(self):
        line = self._file.readline()
        if line:
            return line.strip()
        self._file.close()
        raise StopIteration

    def __str__(self):
        return f"Filer({self.filename})"

    def __add__(self, other):
        new_file = f"concat_{os.path.basename(self.filename)}_{os.path.basename(other.filename)}.txt"
        with open(new_file, 'w') as wf:
            for line in self.line_generator():
                wf.write(line + "\n")
            for line in other.line_generator():
                wf.write(line + "\n")
        return Filer(new_file)

    @staticmethod
    def supported_extensions():
        return ['.txt']

    @classmethod
    def from_path(cls, path: str):
        return cls(path)

class AdvancedFiler(Filer):
    def __init__(self, filename: str):
        super().__init__(filename)

    def concat_files(self, *others):
        new_file = f"multi_concat_{os.path.basename(self.filename)}.txt"
        with open(new_file, 'w') as wf:
            for line in self.line_generator():
                wf.write(line + "\n")
            for other in others:
                for line in other.line_generator():
                    wf.write(line + "\n")
        return Filer(new_file)

    def average(self):
        numbers = [float(line) for line in self.line_generator() if line.strip().isdigit()]
        return sum(numbers) / len(numbers) if numbers else 0

    def __str__(self):
        return f"AdvancedFiler({self.filename})"

    @deco("green")
    def show_content(self):
        for line in self.line_generator():
            print(line)
