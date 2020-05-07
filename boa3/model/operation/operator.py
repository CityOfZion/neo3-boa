from enum import Enum


class Operator(str, Enum):
    # Arithmetic operators
    Plus = '+'
    Minus = '-'
    Mult = '*'
    Div = '/'
    IntDiv = '//'
    Mod = '%'
    Pow = '**'

    def __str__(self) -> str:
        return self.value
