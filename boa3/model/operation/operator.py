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

    # Relational operators
    Eq = '=='
    NotEq = '!='
    Lt = '<'
    LtE = '<='
    Gt = '>'
    GtE = '>='
    Is = 'is'
    IsNot = 'is not'

    # Logical operators
    And = 'and'
    Or = 'or'
    Not = 'not'
    BitAnd = '&'
    BitOr = '|'
    BitNot = '~'
    BitXor = '^'
    LeftShift = '<<'
    RightShift = '>>'

    # Other operators
    Subscript = '[]'

    def __str__(self) -> str:
        return self.value
