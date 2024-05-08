import ast
from enum import Enum
from typing import Self


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
    In = 'in'
    NotIn = 'not in'

    @classmethod
    def get_operation(cls, node: ast.operator) -> Self | None:
        operators: dict[type[ast.operator], Operator] = {
            ast.Add: Operator.Plus,
            ast.Sub: Operator.Minus,
            ast.Mult: Operator.Mult,
            ast.Div: Operator.Div,
            ast.FloorDiv: Operator.IntDiv,
            ast.Mod: Operator.Mod,
            ast.Pow: Operator.Pow,
            ast.UAdd: Operator.Plus,
            ast.USub: Operator.Minus,
            ast.Eq: Operator.Eq,
            ast.NotEq: Operator.NotEq,
            ast.Lt: Operator.Lt,
            ast.LtE: Operator.LtE,
            ast.Gt: Operator.Gt,
            ast.GtE: Operator.GtE,
            ast.Is: Operator.Is,
            ast.IsNot: Operator.IsNot,
            ast.In: Operator.In,
            ast.NotIn: Operator.NotIn,
            ast.And: Operator.And,
            ast.Or: Operator.Or,
            ast.Not: Operator.Not,
            ast.BitAnd: Operator.BitAnd,
            ast.BitOr: Operator.BitOr,
            ast.BitXor: Operator.BitXor,
            ast.Invert: Operator.BitNot,
            ast.LShift: Operator.LeftShift,
            ast.RShift: Operator.RightShift
        }

        node_type = type(node)
        if node_type in operators:
            return operators[node_type]
        else:
            return None

    def requires_right_operand_for_validation(self) -> bool:
        return self in [Operator.In,
                        Operator.NotIn
                        ]

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value
