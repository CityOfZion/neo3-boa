from abc import ABC


class CompilerWarning(ABC):
    def __init__(self, line: int, col: int):
        self.line: int = line
        self.col: int = col
