from enum import Enum


class Operator(str, Enum):
    Plus = '+'
    Minus = '-'
    Mult = '*'
    Div = '/'
    IntDiv = '//'
    Mod = '%'
    Pow = '**'
